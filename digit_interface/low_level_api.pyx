# SPDX-FileCopyrightText: 2022 Manuel Weiss <manuel.weiss@bht-berlin.de>
#
# SPDX-License-Identifier: MIT

# distutils: language = c++
# cython: language_level=3
# cython: embedsignature=True
# distutils: sources = digit_interface/cpp/low_level_connection_class.cpp digit_interface/cpp/lowlevelapi.c digit_interface/cpp/artl.c
# distutils: undef_macros = NDEBUG




import numpy as np

from libcpp cimport bool
from libc.string cimport memcpy
cimport numpy as np
cimport cython


ctypedef np.int16_t DTYPE_int16_t
ctypedef np.int32_t DTYPE_int32_t


cdef extern from "cpp/lowlevelapi.h":

    ctypedef struct llapi_quaternion_t:
        double w
        double x
        double y
        double z
    
    ctypedef struct llapi_base_t:
        double translation[3]
        llapi_quaternion_t orientation
        double linear_velocity[3]
        double angular_velocity[3]
    # 
    ctypedef struct llapi_imu_t:
        llapi_quaternion_t orientation
        double angular_velocity[3]
        double linear_acceleration[3]
        double magnetic_field[3]
     
    ctypedef struct llapi_motor_obs_t:
        double position[20]
        double velocity[20]
        double torque[20]

    ctypedef struct llapi_joint_t:
        double position[10]
        double velocity[10]
       
    ctypedef struct llapi_observation_python_t:
        double time
        bool error
        llapi_base_t base
        llapi_imu_t imu
        llapi_motor_obs_t motor
        llapi_joint_t joint
        DTYPE_int16_t battery_charge
    
    ctypedef struct llapi_motor_t:
        double torque
        double velocity
        double damping
    
    ctypedef struct llapi_command_t:
        llapi_motor_t motors[20]
        DTYPE_int32_t fallback_opmode
        bool apply_command


cdef extern from 'cpp/low_level_connection_class.hpp':
    cdef cppclass C_LLAPI 'low_level_connection_class':
        C_LLAPI(const char*) except +

        llapi_observation_python_t step (llapi_command_t command)
        llapi_observation_python_t get_observation ()



cdef class DigitLLApi:
    cdef C_LLAPI* c_obj

    cdef public llapi_observation_python_t observation
    cdef public llapi_command_t command

    def __cinit__(self, ip="127.0.0.1"):
        ip_c = ip.encode('utf-8')
        print(ip)
        self.c_obj = new C_LLAPI(ip.encode('utf-8'))

    def __init__(self, ip="127.0.0.1"):
        # self.__cinit__(ip)
        self.observation = llapi_observation_python_t()
        
        
        self.command = llapi_command_t()
        self.command.fallback_opmode = 0
        self.command.apply_command = False
        for i in range(20):
            self.command.motors[i].torque = 0.0
            self.command.motors[i].velocity = 0.0
            self.command.motors[i].damping = 0.0
        



    def step(self, np.ndarray[double, ndim=1] torque=np.zeros(20),  np.ndarray[double, ndim=1] velocity=np.zeros(20),  np.ndarray[double, ndim=1] damping=np.zeros(20), fallback_opmode=0, apply_command=False):

        self.set_command(torque, velocity, damping, fallback_opmode, apply_command)
        observation = self.c_obj.step(self.command)
        self.observation = observation
        return observation

    def set_command(self, np.ndarray[double, ndim=1] torque,  np.ndarray[double, ndim=1] velocity,  np.ndarray[double, ndim=1] damping, fallback_opmode=0, apply_command=True):
        """
        this function is used to set the command to the robot
        """
        
        for i in range(20):
            self.command.motors[i].torque = torque[i]
            self.command.motors[i].velocity = velocity[i]
            self.command.motors[i].damping = damping[i]
        self.command.fallback_opmode = 0
        self.command.apply_command = True

    # def get_observation():
    #     observation = self.c_obj.get_observation()
    #     return observation

    def __dealloc__(self):
        del self.c_obj
