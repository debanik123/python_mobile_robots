import rclpy
from rclpy.node import Node
from nav2_msgs.action import TeachAndRepeat
from geometry_msgs.msg import PoseStamped
import sqlite3


class Navigation(Node):

    def __init__(self):
        super().__init__('navigation')
        self.action_client = self.create_client(TeachAndRepeat, 'teach_and_repeat')
        self.poses = []
        self.load_poses_from_database()

    def load_poses_from_database(self):
        conn = sqlite3.connect('poses.db')
        c = conn.cursor()
        c.execute('SELECT * FROM poses')
        rows = c.fetchall()
        for row in rows:
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.pose.position.x = row[1]
            pose.pose.position.y = row[2]
            pose.pose.position.z = row[3]
            pose.pose.orientation.x = row[4]
            pose.pose.orientation.y = row[5]
            pose.pose.orientation.z = row[6]
            pose.pose.orientation.w = row[7]
            self.poses.append(pose)
        conn.close()

    def send_goal(self):
        goal_msg = TeachAndRepeat.Goal()
        goal_msg.teach = False
        goal_msg.repeat = True
        goal_msg.waypoints = self.poses
        self.action_client.wait_for_server()
        self.action_client.send_goal_async(goal_msg)

    def teach(self):
        goal_msg = TeachAndRepeat.Goal()
        goal_msg.teach = True
        goal_msg.repeat = False
        self.action_client.wait_for_server()
        self.action_client.send_goal_async(goal_msg)
        while True:
            if self.action_client.wait_for_result():
                break

    def main(self):
        self.teach()
        self.send_goal()
        rclpy.spin_until_future_complete(self, self.action_client.goal_result_future)


def main(args=None):
    rclpy.init(args=args)
    navigation = Navigation()
    navigation.main()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
