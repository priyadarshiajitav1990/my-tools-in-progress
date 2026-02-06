
import os
import sys
import filecmp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import proxyendpoint2service
import targetendpoint2service

def test_proxy_target_endpoints():
    proxyendpoint2service.main()
    targetendpoint2service.main()
    assert filecmp.cmp('kong_service.yaml', os.path.join(os.path.dirname(__file__), 'desired_kong_service.yaml'), shallow=False)
    assert filecmp.cmp('kong_route.yaml', os.path.join(os.path.dirname(__file__), 'desired_kong_route.yaml'), shallow=False)

if __name__ == "__main__":
    test_proxy_target_endpoints()
    print("Medium test cases passed.")
