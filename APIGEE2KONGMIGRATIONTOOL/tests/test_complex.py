
import os
import sys
import filecmp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import apigee_policy2rate_limiting
import apigee_policy2oauth2
import apigee_policy2key_auth
import verify_kong_output

def test_complex_policies():
    apigee_policy2rate_limiting.main()
    apigee_policy2oauth2.main()
    apigee_policy2key_auth.main()
    verify_kong_output.main()
    d = os.path.dirname(__file__)
    assert filecmp.cmp('kong_rate_limiting.yaml', os.path.join(d, 'desired_kong_rate_limiting.yaml'), shallow=False)
    assert filecmp.cmp('kong_oauth2.yaml', os.path.join(d, 'desired_kong_oauth2.yaml'), shallow=False)
    assert filecmp.cmp('kong_key_auth.yaml', os.path.join(d, 'desired_kong_key_auth.yaml'), shallow=False)
    assert filecmp.cmp('kong_output_verified.yaml', os.path.join(d, 'desired_kong_output_verified.yaml'), shallow=False)

if __name__ == "__main__":
    test_complex_policies()
    print("Complex test cases passed.")
