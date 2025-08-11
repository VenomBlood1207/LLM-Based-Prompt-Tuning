#!/usr/bin/env python3
"""
Memory usage testing for Ollama models
Run this to benchmark memory consumption of different models
"""

import requests
import json
import time
import psutil
import subprocess
import threading
from typing import Dict, List

class ModelTester:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.results = {}
        
    def get_gpu_memory(self) -> float:
        """Get current GPU memory usage in MB"""
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True)
            return float(result.stdout.strip())
        except:
            return 0.0
    
    def get_system_memory(self) -> float:
        """Get current system RAM usage in MB"""
        return psutil.virtual_memory().used / (1024 * 1024)
    
    def test_model_loading(self, model_name: str) -> Dict:
        """Test memory usage when loading a model"""
        print(f"\n=== Testing {model_name} ===")
        
        # Get baseline memory
        baseline_gpu = self.get_gpu_memory()
        baseline_ram = self.get_system_memory()
        
        print(f"Baseline - GPU: {baseline_gpu:.0f}MB, RAM: {baseline_ram:.0f}MB")
        
        # Load model with a simple prompt
        test_prompt = "Hello, how are you today?"
        
        start_time = time.time()
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", 
                                   json={
                                       "model": model_name,
                                       "prompt": test_prompt,
                                       "stream": False
                                   }, 
                                   timeout=120)
            
            load_time = time.time() - start_time
            
            # Get memory after loading
            loaded_gpu = self.get_gpu_memory()
            loaded_ram = self.get_system_memory()
            
            gpu_usage = loaded_gpu - baseline_gpu
            ram_usage = loaded_ram - baseline_ram
            
            # Test response quality
            if response.status_code == 200:
                response_data = response.json()
                response_text = response_data.get('response', '')
                success = True
            else:
                response_text = f"Error: {response.status_code}"
                success = False
            
            result = {
                'success': success,
                'load_time': load_time,
                'gpu_memory_mb': gpu_usage,
                'ram_memory_mb': ram_usage,
                'total_gpu_mb': loaded_gpu,
                'total_ram_mb': loaded_ram,
                'response_length': len(response_text),
                'sample_response': response_text[:100] + "..." if len(response_text) > 100 else response_text
            }
            
            print(f"Success: {success}")
            print(f"Load time: {load_time:.2f}s")
            print(f"GPU usage: +{gpu_usage:.0f}MB (Total: {loaded_gpu:.0f}MB)")
            print(f"RAM usage: +{ram_usage:.0f}MB (Total: {loaded_ram:.0f}MB)")
            print(f"Response: {result['sample_response']}")
            
            return result
            
        except Exception as e:
            print(f"Error testing {model_name}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'load_time': time.time() - start_time
            }
    
    def test_concurrent_models(self, model1: str, model2: str) -> Dict:
        """Test running two models simultaneously"""
        print(f"\n=== Testing Concurrent: {model1} + {model2} ===")
        
        baseline_gpu = self.get_gpu_memory()
        baseline_ram = self.get_system_memory()
        
        results = {'model1': None, 'model2': None, 'success': False}
        
        def run_model(model_name: str, prompt: str, result_key: str):
            try:
                response = requests.post(f"{self.base_url}/api/generate",
                                       json={
                                           "model": model_name,
                                           "prompt": prompt,
                                           "stream": False
                                       },
                                       timeout=60)
                
                if response.status_code == 200:
                    results[result_key] = {
                        'success': True,
                        'response': response.json().get('response', '')[:50]
                    }
                else:
                    results[result_key] = {'success': False, 'error': response.status_code}
                    
            except Exception as e:
                results[result_key] = {'success': False, 'error': str(e)}
        
        # Start both models concurrently
        start_time = time.time()
        
        thread1 = threading.Thread(target=run_model, args=(model1, "What is AI?", 'model1'))
        thread2 = threading.Thread(target=run_model, args=(model2, "Explain machine learning briefly.", 'model2'))
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        total_time = time.time() - start_time
        final_gpu = self.get_gpu_memory()
        final_ram = self.get_system_memory()
        
        concurrent_result = {
            'total_time': total_time,
            'gpu_usage': final_gpu - baseline_gpu,
            'ram_usage': final_ram - baseline_ram,
            'total_gpu': final_gpu,
            'total_ram': final_ram,
            'model1_success': results['model1']['success'] if results['model1'] else False,
            'model2_success': results['model2']['success'] if results['model2'] else False,
            'overall_success': (results['model1'] and results['model1']['success'] and 
                              results['model2'] and results['model2']['success'])
        }
        
        print(f"Concurrent execution time: {total_time:.2f}s")
        print(f"Total GPU usage: {concurrent_result['gpu_usage']:.0f}MB ({final_gpu:.0f}MB total)")
        print(f"Total RAM usage: {concurrent_result['ram_usage']:.0f}MB ({final_ram:.0f}MB total)")
        print(f"Model1 success: {concurrent_result['model1_success']}")
        print(f"Model2 success: {concurrent_result['model2_success']}")
        print(f"Overall success: {concurrent_result['overall_success']}")
        
        return concurrent_result
    
    def run_full_benchmark(self):
        """Run complete benchmark suite"""
        models_to_test = [
            "llama3.1:8b",
            "mistral:7b", 
            "llama3.2:3b",
            "phi3:3.8b",
            "gemma:2b"
        ]
        
        print("Starting comprehensive model testing...")
        print("=" * 50)
        
        # Test individual models
        for model in models_to_test:
            self.results[model] = self.test_model_loading(model)
            time.sleep(5)  # Cool down between tests
        
        # Test promising concurrent combinations
        concurrent_tests = [
            ("llama3.2:7b", "llama3.2:3b"),
            ("llama3.2:7b", "phi3:3.8b"),
            ("mistral:7b", "llama3.2:3b"),
            ("mistral:7b", "phi3:3.8b")
        ]
        
        self.results['concurrent'] = {}
        for model1, model2 in concurrent_tests:
            key = f"{model1}+{model2}"
            self.results['concurrent'][key] = self.test_concurrent_models(model1, model2)
            time.sleep(10)  # Longer cool down for concurrent tests
    
    def generate_report(self):
        """Generate a summary report"""
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY REPORT")
        print("=" * 60)
        
        print("\nINDIVIDUAL MODEL PERFORMANCE:")
        print("-" * 40)
        for model, result in self.results.items():
            if model != 'concurrent' and result.get('success'):
                print(f"{model}:")
                print(f"  Load time: {result['load_time']:.2f}s")
                print(f"  GPU memory: {result['gpu_memory_mb']:.0f}MB")
                print(f"  RAM memory: {result['ram_memory_mb']:.0f}MB")
                print(f"  Response quality: {'Good' if result['response_length'] > 20 else 'Short'}")
                print()
        
        if 'concurrent' in self.results:
            print("CONCURRENT MODEL PERFORMANCE:")
            print("-" * 40)
            for combo, result in self.results['concurrent'].items():
                if result['overall_success']:
                    print(f"{combo}:")
                    print(f"  Execution time: {result['total_time']:.2f}s")
                    print(f"  Total GPU usage: {result['gpu_usage']:.0f}MB")
                    print(f"  Status: {'✓ RECOMMENDED' if result['total_gpu'] < 7500 else '⚠ HIGH MEMORY'}")
                    print()
        
        # Save results to file
        with open('model_benchmark_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("Results saved to 'model_benchmark_results.json'")

if __name__ == "__main__":
    tester = ModelTester()
    
    print("GPU Memory Benchmark Tool")
    print("Make sure Ollama is running: 'ollama serve'")
    print()
    
    # Quick connectivity test
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Ollama connection successful")
        else:
            print("✗ Ollama connection failed")
            exit(1)
    except:
        print("✗ Cannot connect to Ollama. Make sure it's running.")
        exit(1)
    
    tester.run_full_benchmark()
    tester.generate_report()
