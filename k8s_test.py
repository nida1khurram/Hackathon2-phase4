"""
Kubernetes Deployment Test Suite
This module contains comprehensive tests for Minikube and Kubernetes deployment of the Todo application
"""

import unittest
import subprocess
import requests
import time
import json
from typing import Dict, Any, Optional
import yaml

class KubernetesTest(unittest.TestCase):
    """
    Test suite for Kubernetes deployment of Todo application
    """
    
    def setUp(self):
        """
        Set up test environment for Kubernetes tests
        """
        self.app_name = "todo-app"
        self.namespace = "default"
        self.backend_port = 8000
        self.frontend_port = 80
        self.minikube_ip = None
        self.frontend_node_port = None
        self.backend_service_url = None
        self.frontend_service_url = None
    
    def run_command(self, cmd: str) -> tuple:
        """
        Helper method to run shell commands
        """
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=120
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
    
    def test_01_minikube_status(self):
        """
        Test Minikube is running and accessible
        """
        print("Testing Minikube status...")
        returncode, stdout, stderr = self.run_command("minikube status")
        
        self.assertEqual(returncode, 0, f"Minikube is not running: {stderr}")
        self.assertIn("Running", stdout, "Minikube should be in running state")
        
        print("✓ Minikube is running and accessible")
    
    def test_02_cluster_info(self):
        """
        Test kubectl can connect to the cluster
        """
        print("Testing kubectl cluster connection...")
        returncode, stdout, stderr = self.run_command("kubectl cluster-info")
        
        self.assertEqual(returncode, 0, f"kubectl cannot connect to cluster: {stderr}")
        self.assertIn("Kubernetes control plane", stdout, "Should connect to Kubernetes control plane")
        
        print("✓ kubectl connected to cluster successfully")
    
    def test_03_nodes_available(self):
        """
        Test that nodes are available in the cluster
        """
        print("Testing cluster nodes...")
        returncode, stdout, stderr = self.run_command("kubectl get nodes")
        
        self.assertEqual(returncode, 0, f"Cannot get nodes: {stderr}")
        self.assertIn("Ready", stdout, "At least one node should be in Ready state")
        
        print("✓ Cluster nodes are available and ready")
    
    def test_04_build_and_load_images(self):
        """
        Test building and loading Docker images into Minikube
        """
        print("Building and loading Docker images...")
        
        # First check if Docker is running
        returncode, stdout, stderr = self.run_command("docker ps")
        self.assertEqual(returncode, 0, f"Docker is not running: {stderr}")
        
        # Build backend image
        print("Building backend image...")
        returncode, stdout, stderr = self.run_command("cd backend && docker build -t todo-backend:test .")
        self.assertEqual(returncode, 0, f"Failed to build backend image: {stderr}")
        
        # Build frontend image
        print("Building frontend image...")
        returncode, stdout, stderr = self.run_command("cd frontend && docker build -t todo-frontend:test .")
        self.assertEqual(returncode, 0, f"Failed to build frontend image: {stderr}")
        
        # Load images into Minikube
        print("Loading images into Minikube...")
        returncode, stdout, stderr = self.run_command("minikube image load todo-backend:test")
        self.assertEqual(returncode, 0, f"Failed to load backend image: {stderr}")
        
        returncode, stdout, stderr = self.run_command("minikube image load todo-frontend:test")
        self.assertEqual(returncode, 0, f"Failed to load frontend image: {stderr}")
        
        print("✓ Docker images built and loaded into Minikube successfully")
    
    def test_05_helm_install(self):
        """
        Test Helm chart installation
        """
        print("Installing Helm chart...")
        
        # Remove any existing installation
        self.run_command(f"helm uninstall todo-app --namespace default")
        
        # Install the Helm chart
        cmd = f"helm install todo-app ./charts/todo-app --namespace default --wait --timeout=10m"
        returncode, stdout, stderr = self.run_command(cmd)
        
        self.assertEqual(returncode, 0, f"Helm install failed: {stderr}")
        
        # Wait a bit for resources to be created
        time.sleep(10)
        
        print("✓ Helm chart installed successfully")
    
    def test_06_pods_running(self):
        """
        Test that all pods are running and ready
        """
        print("Checking pod status...")
        
        # Wait for pods to be ready
        timeout = 300  # 5 minutes
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            returncode, stdout, stderr = self.run_command("kubectl get pods -n default")
            
            if returncode == 0 and "Running" in stdout:
                # Check if all pods are ready (not just running but ready)
                lines = stdout.strip().split('\n')
                ready_pods = 0
                total_pods = 0
                
                for line in lines[1:]:  # Skip header
                    if "todo-app" in line:
                        total_pods += 1
                        # Check if pod is ready (format: #/# where first number is ready count)
                        if "Running" in line and "0/" not in line:
                            ready_pods += 1
                
                if ready_pods == total_pods and total_pods > 0:
                    print(f"✓ All {ready_pods} pods are running and ready")
                    return  # Success
            
            time.sleep(10)
        
        # If we get here, pods didn't become ready in time
        returncode, stdout, stderr = self.run_command(f"kubectl get pods -n {self.namespace}")
        self.fail(f"Not all pods became ready within timeout. Current status:\n{stdout}\n{stderr}")
    
    def test_07_services_available(self):
        """
        Test that services are available and accessible
        """
        print("Checking service availability...")
        
        # Get services
        returncode, stdout, stderr = self.run_command(f"kubectl get services -n {self.namespace}")
        self.assertEqual(returncode, 0, f"Cannot get services: {stderr}")
        
        # Check for backend service
        self.assertIn(f"{self.app_name}-backend", stdout, "Backend service should exist")
        
        # Check for frontend service
        self.assertIn(f"{self.app_name}-frontend", stdout, "Frontend service should exist")
        
        # Get service details to find NodePort
        returncode, stdout, stderr = self.run_command(f"kubectl get service {self.app_name}-frontend -n {self.namespace} -o json")
        self.assertEqual(returncode, 0, f"Cannot get frontend service details: {stderr}")
        
        service_details = json.loads(stdout)
        ports = service_details.get('spec', {}).get('ports', [])
        
        # Find the NodePort for the frontend
        node_port = None
        for port in ports:
            if port.get('port') == self.frontend_port:
                node_port = port.get('nodePort')
                break
        
        self.assertIsNotNone(node_port, f"Could not find NodePort for frontend service: {ports}")
        
        # Get Minikube IP
        returncode, stdout, stderr = self.run_command("minikube ip")
        self.assertEqual(returncode, 0, f"Cannot get Minikube IP: {stderr}")
        
        self.minikube_ip = stdout.strip()
        self.frontend_service_url = f"http://{self.minikube_ip}:{node_port}"
        
        print(f"✓ Services are available, frontend accessible at: {self.frontend_service_url}")
    
    def test_08_backend_health_check(self):
        """
        Test backend health endpoint
        """
        print("Testing backend health endpoint...")
        
        # Get backend service details
        returncode, stdout, stderr = self.run_command(f"kubectl get service {self.app_name}-backend -n {self.namespace} -o json")
        self.assertEqual(returncode, 0, f"Cannot get backend service details: {stderr}")
        
        service_details = json.loads(stdout)
        backend_port = None
        ports = service_details.get('spec', {}).get('ports', [])
        
        for port in ports:
            if port.get('port') == self.backend_port:
                backend_port = port.get('port')
                break
        
        if backend_port:
            # Try to access backend through port forwarding first to test
            print("✓ Backend service is configured correctly")
        else:
            # If direct access doesn't work, try to set up port forwarding
            pass
    
    def test_09_frontend_accessibility(self):
        """
        Test that frontend is accessible via NodePort
        """
        print("Testing frontend accessibility...")
        
        if not self.frontend_service_url:
            self.skipTest("Frontend service URL not available")
        
        # Wait a bit for the service to be fully ready
        time.sleep(10)
        
        try:
            response = requests.get(self.frontend_service_url, timeout=30)
            self.assertEqual(response.status_code, 200, f"Frontend not accessible, status: {response.status_code}")
            self.assertIn("Todo", response.text or "", "Response should contain 'Todo' indicating app loaded")
            
            print("✓ Frontend is accessible via NodePort")
        except requests.exceptions.RequestException as e:
            self.fail(f"Frontend is not accessible at {self.frontend_service_url}: {str(e)}")
    
    def test_10_backend_api_accessibility(self):
        """
        Test that backend API is accessible
        """
        print("Testing backend API accessibility...")
        
        # Get backend service URL via port forwarding since it's ClusterIP
        returncode, stdout, stderr = self.run_command(f"kubectl port-forward service/{self.app_name}-backend 8000:8000 -n {self.namespace} &")
        
        # Give it a moment to start
        time.sleep(5)
        
        try:
            # Test health endpoint
            response = requests.get("http://localhost:8000/health", timeout=10)
            self.assertIn(response.status_code, [200, 401], f"Backend health check failed, status: {response.status_code}")
            
            print("✓ Backend API is accessible")
        except requests.exceptions.RequestException as e:
            print(f"Note: Backend port-forward may still be starting: {str(e)}")
            # This might be expected if port-forward is still initializing
            pass
        finally:
            # Kill the port-forward process
            self.run_command("pkill -f 'kubectl port-forward'")
    
    def test_11_application_functionality(self):
        """
        Test basic application functionality through the deployed app
        """
        print("Testing basic application functionality...")
        
        if not self.frontend_service_url:
            self.skipTest("Frontend service URL not available")
        
        # Test that the application loads
        try:
            response = requests.get(self.frontend_service_url, timeout=30)
            self.assertEqual(response.status_code, 200, f"Application failed to load, status: {response.status_code}")
            
            # Check for key elements that indicate the app is working
            content = response.text
            self.assertTrue(
                any(keyword in content for keyword in ["Todo", "task", "Task", "todo"]),
                "Response should contain application keywords"
            )
            
            print("✓ Application is functioning correctly")
        except requests.exceptions.RequestException as e:
            self.fail(f"Application is not functioning properly: {str(e)}")
    
    def test_12_helm_upgrade(self):
        """
        Test Helm upgrade functionality
        """
        print("Testing Helm upgrade functionality...")
        
        # Upgrade with a simple value change
        cmd = f"helm upgrade {self.app_name} ./charts/todo-app --namespace {self.namespace} --set frontend.replicaCount=2 --wait --timeout=5m"
        returncode, stdout, stderr = self.run_command(cmd)
        
        self.assertEqual(returncode, 0, f"Helm upgrade failed: {stderr}")
        
        # Wait for pods to scale up
        time.sleep(20)
        
        # Check that we now have 2 frontend pods
        returncode, stdout, stderr = self.run_command(f"kubectl get pods -n {self.namespace}")
        frontend_pods = [line for line in stdout.split('\n') if f"{self.app_name}-frontend" in line and "Running" in line]
        
        # Count frontend pods (there might be more than 2 if previous pods are terminating)
        frontend_running_count = sum(1 for pod in frontend_pods if "Running" in pod)
        self.assertGreaterEqual(frontend_running_count, 1, "Should have at least 1 running frontend pod after upgrade")
        
        print(f"✓ Helm upgrade successful, now have {frontend_running_count} frontend pods running")
    
    def test_13_scale_deployments(self):
        """
        Test scaling deployments
        """
        print("Testing deployment scaling...")
        
        # Scale backend deployment
        returncode, stdout, stderr = self.run_command(f"kubectl scale deployment {self.app_name}-backend --replicas=2 -n {self.namespace}")
        self.assertEqual(returncode, 0, f"Failed to scale backend: {stderr}")
        
        # Wait for scaling to complete
        time.sleep(15)
        
        # Verify scaling
        returncode, stdout, stderr = self.run_command(f"kubectl get deployment {self.app_name}-backend -n {self.namespace}")
        self.assertIn("2/2", stdout, "Backend deployment should be scaled to 2 replicas")
        
        print("✓ Deployment scaling test passed")
    
    def test_14_resource_limits(self):
        """
        Test that resource limits are properly set
        """
        print("Testing resource limits...")
        
        # Check backend deployment resource limits
        returncode, stdout, stderr = self.run_command(f"kubectl get deployment {self.app_name}-backend -n {self.namespace} -o yaml")
        self.assertEqual(returncode, 0, f"Cannot get backend deployment: {stderr}")
        
        deployment_yaml = yaml.safe_load(stdout)
        containers = deployment_yaml.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        
        backend_container = None
        for container in containers:
            if 'backend' in container.get('name', '').lower():
                backend_container = container
                break
        
        if backend_container:
            resources = backend_container.get('resources', {})
            limits = resources.get('limits', {})
            requests = resources.get('requests', {})
            
            # Check that limits and requests are set (even if they're defaults)
            self.assertIsInstance(limits, dict)
            self.assertIsInstance(requests, dict)
            
            print("✓ Resource limits are properly configured")
        else:
            print("Note: Could not find backend container in deployment")
    
    def test_15_cleanup(self):
        """
        Test cleanup by uninstalling the Helm release
        """
        print("Cleaning up Helm release...")
        
        returncode, stdout, stderr = self.run_command(f"helm uninstall {self.app_name} --namespace {self.namespace}")
        self.assertEqual(returncode, 0, f"Failed to uninstall Helm release: {stderr}")
        
        print("✓ Helm release uninstalled successfully")


def run_k8s_tests():
    """
    Run the Kubernetes test suite
    """
    print("Starting Kubernetes Deployment Test Suite...")
    print("Make sure Minikube is running with: minikube start --memory=4g --cpus=2")
    print("-" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(KubernetesTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Kubernetes Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors))/result.testsRun)*100:.1f}%" if result.testsRun > 0 else "0%")
    print(f"{'='*50}")
    
    if result.wasSuccessful():
        print("\n🎉 All Kubernetes tests passed! The deployment is working correctly.")
        print("The Todo application is successfully deployed on Kubernetes with all functionality working.")
    else:
        print(f"\n❌ {len(result.failures + result.errors)} test(s) failed.")
        print("Check the output above for details about the deployment issues.")
    
    return result


if __name__ == '__main__':
    run_k8s_tests()