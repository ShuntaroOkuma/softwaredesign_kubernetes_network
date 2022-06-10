from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_info():
    	hostname = subprocess.check_output('hostname').decode(encoding='utf-8').replace('\n','')
    	host_command = ["kubectl", "get", "pods", hostname, "-o=jsonpath='{.status.hostIP}'"]
    	pod_command  = ["kubectl", "get", "pods", hostname, "-o=jsonpath='{.status.podIP}'"]
    	hostIp = subprocess.check_output(host_command).decode(encoding='utf-8').replace('\n','')
    	podIp = subprocess.check_output(pod_command).decode(encoding='utf-8').replace('\n','')
    	return f"pod ip: {podIp}, node ip: {hostIp}\n"
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
