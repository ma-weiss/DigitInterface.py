#include "low_level_connection_class.hpp"

low_level_connection_class::low_level_connection_class(
    const char* publisher_address) {
   llapi_init(publisher_address);
   this->command.apply_command = false;
   while (!llapi_get_observation(&this->observation))
      llapi_send_command(&this->command);

   limits = llapi_get_limits();
}

llapi_observation_python_t low_level_connection_class::step(
    llapi_command_t command) {
   llapi_send_command(&this->command);
   if (!llapi_connected()) {
      // Handle error case. You don't need to re-initialize subscriber
      // Calling llapi_send_command will keep low level api open
   }

   int return_val = llapi_get_observation(&this->observation);
   if (return_val < 1) {
      // Error occurred
   } else if (return_val) {
      // New data received
   } else {
      // No new data
   }
   convert_to_python_observation();

   llapi_send_command(&command);
   if (!llapi_connected()) {
      // Handle error case. You don't need to re-initialize subscriber
      // Calling llapi_send_command will keep low level api open
   }
   this->command = command;
   return this->observation_python;
}


llapi_observation_python_t low_level_connection_class::get_observation()
{
    return this->observation_python;
}

void low_level_connection_class::convert_to_python_observation()
{
    this->observation_python.time = this->observation.time;
   this->observation_python.error = this->observation.error;

   this->observation_python.base.orientation.w =
       this->observation.base.orientation.w;
   this->observation_python.base.orientation.x =
       this->observation.base.orientation.x;
   this->observation_python.base.orientation.y =
       this->observation.base.orientation.y;
   this->observation_python.base.orientation.z =
       this->observation.base.orientation.z;

   this->observation_python.imu.orientation.w =
       this->observation.imu.orientation.w;
   this->observation_python.imu.orientation.x =
       this->observation.imu.orientation.x;
   this->observation_python.imu.orientation.y =
       this->observation.imu.orientation.y;
   this->observation_python.imu.orientation.z =
       this->observation.imu.orientation.z;

   for (int i = 0; i < 3; i++) {
      this->observation_python.base.translation[i] =
          this->observation.base.translation[i];
      this->observation_python.base.linear_velocity[i] =
          this->observation.base.linear_velocity[i];
      this->observation_python.base.angular_velocity[i] =
          this->observation.base.angular_velocity[i];

      this->observation_python.imu.angular_velocity[i] =
          this->observation.imu.angular_velocity[i];
      this->observation_python.imu.linear_acceleration[i] =
          this->observation.imu.linear_acceleration[i];
      this->observation_python.imu.magnetic_field[i] =
          this->observation.imu.magnetic_field[i];
   }
   for (int i = 0; i < NUM_MOTORS; i++) {
      this->observation_python.motor.position[i] =
          this->observation.motor.position[i];
      this->observation_python.motor.velocity[i] =
          this->observation.motor.velocity[i];
      this->observation_python.motor.torque[i] =
          this->observation.motor.torque[i];
   }
   for (int i = 0; i < NUM_JOINTS; i++) {
      this->observation_python.joint.position[i] =
          this->observation.joint.position[i];
      this->observation_python.joint.velocity[i] =
          this->observation.joint.velocity[i];
   }

   // this->observation_python.imu = this->observation.imu;
   // this->observation_python.motor = this->observation.motor;
   // this->observation_python.joint = this->observation.joint;
   this->observation_python.battery_charge = this->observation.battery_charge;

}



low_level_connection_class::~low_level_connection_class() {}
