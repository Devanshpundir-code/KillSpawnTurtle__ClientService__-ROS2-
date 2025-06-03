import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import TurnON



class Activator(Node):
    def __init__(self, node_name, *, context = None, cli_args = None, namespace = None, use_global_arguments = True, enable_rosout = True, start_parameter_services = True, parameter_overrides = None, allow_undeclared_parameters = False, automatically_declare_parameters_from_overrides = False, enable_logger_service = False):
        super().__init__(node_name, context=context, cli_args=cli_args, namespace=namespace, use_global_arguments=use_global_arguments, enable_rosout=enable_rosout, start_parameter_services=start_parameter_services, parameter_overrides=parameter_overrides, allow_undeclared_parameters=allow_undeclared_parameters, automatically_declare_parameters_from_overrides=automatically_declare_parameters_from_overrides, enable_logger_service=enable_logger_service)
        self.client_ = self.create_client(TurnON, "activator")

    def call_activate(self, value):
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for the server")

        request = TurnON.Request()
        request.status = value

        future = self.client_.call_async(request)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        response = future.result()
        self.get_logger().info("Success status"+ str(response.success))
        self.get_logger().info("Success status"+ response.message)

        
def main(args=None):
    rclpy.init()
    node = Activator("nodename_client")
    node.call_activate(0)
    rclpy.spin(node)
    rclpy.shutdown()
