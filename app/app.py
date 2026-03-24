from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'status': 'healthy',
            'platform': 'Kubernetes + ArgoCD GitOps',
            'automation': 'Ansible Automation Platform',
            'monitoring': 'Prometheus + Grafana',
            'ai': 'Ollama / Llama3 - Red Hat AI Platform'
        }
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    print('Server running on port 8080')
    HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
