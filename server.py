import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from my_robot_interfaces.srv import TurnON



class ActiveServer(Node):
    def __init__(self, node_name, *, context = None, cli_args = None, namespace = None, use_global_arguments = True, enable_rosout = True, start_parameter_services = True, parameter_overrides = None, allow_undeclared_parameters = False, automatically_declare_parameters_from_overrides = False, enable_logger_service = False):
        super().__init__(node_name, context=context, cli_args=cli_args, namespace=namespace, use_global_arguments=use_global_arguments, enable_rosout=enable_rosout, start_parameter_services=start_parameter_services, parameter_overrides=parameter_overrides, allow_undeclared_parameters=allow_undeclared_parameters, automatically_declare_parameters_from_overrides=automatically_declare_parameters_from_overrides, enable_logger_service=enable_logger_service)
        self.server_ = self.create_service(TurnON, "activator", self.getinfo_callback)
        self.client_kill = self.create_client(Kill,'kill')
        self.client_spawn = self.create_client(Spawn,'spawn')


    def getinfo_callback(self,request: TurnON.Request, response: TurnON.Response):
        if request.status == 1:
            self.get_logger().info("Received ON request. Spawning turtle.")
            self.req_on_callback()
            response.success = True
            response.message = "turtle1 is spawned"

        elif request.status == 0:
            self.get_logger().info("Received Of request. Despawning turtle.")
            response.success = True
            response.message = "turtle1 is killed"
            self.req_of_callback()
        return response
    #now defining the above funtions
    #these funtions are for the clients
    def req_of_callback(self):
        while not self.client_kill.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for the kill service")

        request = Kill.Request()
        request.name = "turtle1"

        future = self.client_kill.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info("Turtle killed successfully.")
        else:
            self.get_logger().error("Failed to kill turtle.")

        

        self.client_spawn.call_async(request)
    def req_of_callback(self):
        while not self.client_kill.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for the kill service")

        request = Kill.Request()
        request.name = "turtle1"

        future = self.client_kill.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info("Turtle killed successfully.")
        else:
            self.get_logger().error("Failed to kill turtle.")

        

def main(args=None):
    rclpy.init(args=args)
    node = ActiveServer("node_name_servr")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


