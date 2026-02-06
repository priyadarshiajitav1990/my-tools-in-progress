
import os
import sys
import filecmp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import apigee_policy2javascriptplugin
import apigee_policy2jspolicy

def test_javascriptplugin():
    apigee_policy2javascriptplugin.main()
    assert filecmp.cmp('kong_javascriptplugin.yaml', os.path.join(os.path.dirname(__file__), 'desired_kong_javascriptplugin.yaml'), shallow=False)

def test_jspolicy():
    apigee_policy2jspolicy.main()
    assert filecmp.cmp('kong_jspolicy.yaml', os.path.join(os.path.dirname(__file__), 'desired_kong_jspolicy.yaml'), shallow=False)

if __name__ == "__main__":
    test_javascriptplugin()
    test_jspolicy()
    print("Simple test cases passed.")
