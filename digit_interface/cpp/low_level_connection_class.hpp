#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "lowlevelapi.h"

typedef struct {
   double translation[3];
   llapi_quaternion_t orientation;
   double linear_velocity[3];
   double angular_velocity[3];
} llapi_base_t;

typedef struct {
   llapi_quaternion_t orientation;
   double angular_velocity[3];
   double linear_acceleration[3];
   double magnetic_field[3];
} llapi_imu_t;

typedef struct {
   double position[NUM_MOTORS];
   double velocity[NUM_MOTORS];
   double torque[NUM_MOTORS];
} llapi_motor_obs_t;

typedef struct {
   double position[NUM_JOINTS];
   double velocity[NUM_JOINTS];
} llapi_joint_t;

typedef struct {
   // All values are in SI units (N-m, rad, rad/s, V). Temperature is in deg C

   // Time since control program started
   double time;

   // Robot status flag. Monitor the JSON API for details if flag is set to true
   // If false: robot is operating normally
   // If true:  An issue occurred that causes the system to have reduced
   //           performance, or a fatal issue may occur unless the user does
   //           something. The system will automatically disable the Low-level
   //           API after a brief delay. This delay can be read by calling
   //           llapi_get_error_shutdown_delay().
   bool error;

   // Estimated pose and velocity of base frame

   llapi_base_t base;
   // Raw sensor signals from IMU
   llapi_imu_t imu;

   // Actuated joints
   llapi_motor_obs_t motor;

   // Unactuated joints
   llapi_joint_t joint;

   // Expressed as percent (0-100)
   int16_t battery_charge;

} llapi_observation_python_t;
int llapi_observation_python(llapi_observation_python_t* obs);

class low_level_connection_class {
  private:
   llapi_command_t command = {0};
   llapi_observation_t observation;
   llapi_observation_python_t observation_python;
   const llapi_limits_t* limits;

  public:
   low_level_connection_class(const char* publisher_address);

   ~low_level_connection_class();
   llapi_observation_python_t step(llapi_command_t command);
};
