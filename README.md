# scancode-plugins
Plugins for Running scancode on RoCm

# To Install the Plugins
Go to the Plugin Directory
'''cd scancode-toolkit/plugins/scancode-licence-modifications'''

# Run following command
 '''pip install -e .'''




# Example : 

'''scancode -clpeui  --package --processes 64 --license-text --verbose --full-root --json-pp roctracer.json ../roctracer --license-policy ../amd_licence_policy.yml --classify --summary --summary-with-details  --license-diag --no-licenses --licence-modifications'''


# To Create HTML reporved of approved, not approved and license modification html report


scancode -clpeui  --package --processes 64 --classify --verbose --full-root --json-pp roctracer.json ../roctracer  --license-policy ../amd_licence_policy.yml  --summary --summary-with-details --license-text --license-text-diagnostics --is-license-text  --license-diag --no-licenses --licence-modifications --custom-output white-black-report.html --custom-template white-black.html
