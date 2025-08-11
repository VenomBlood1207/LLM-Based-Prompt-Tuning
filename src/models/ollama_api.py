import requests
import json
import logging

class OllamaAPI:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        
    def generate_response(self, model: str, prompt: str, params: dict = None):
        """Basic generation endpoint"""
        try:
            endpoint = f"{self.base_url}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,  # Important: disable streaming
                **(params or {})
            }
            
            response = requests.post(endpoint, json=payload)
            
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError as e:
                    # Handle streaming response format
                    responses = []
                    for line in response.text.strip().split('\n'):
                        try:
                            if line:
                                responses.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
                    
                    if responses:
                        # Combine responses
                        combined_response = {
                            "response": "".join(r.get("response", "") for r in responses),
                            "model": model,
                            "created_at": responses[0].get("created_at", "")
                        }
                        return combined_response
                    
            self.logger.error(f"API error: {response.status_code}")
            return None
            
        except Exception as e:
            self.logger.error(f"Generation error: {str(e)}")
            return None
            
    def test_connection(self):
        """Test API connectivity"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
