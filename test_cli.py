#!/usr/bin/env python3
"""
Simple test script for A2A CLI

Tests basic functionality without requiring a running A2A system.
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the current directory to the path to import a2a_cli
sys.path.insert(0, str(Path(__file__).parent))

try:
    from a2a_cli import A2AConfig, A2AClient, print_table
    import click
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you've installed the requirements: pip install -r requirements.txt")
    sys.exit(1)

class TestA2AConfig(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = A2AConfig()
    
    def test_default_config(self):
        """Test default configuration values"""
        self.assertEqual(self.config.get("registry_url"), "http://localhost:8000")
        self.assertEqual(self.config.get("log_level"), "INFO")
        self.assertEqual(self.config.get("timeout"), 30)
    
    def test_config_get_set(self):
        """Test setting and getting configuration values"""
        self.config.set("test_key", "test_value")
        self.assertEqual(self.config.get("test_key"), "test_value")

class TestA2AClient(unittest.TestCase):
    """Test A2A client functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = A2AConfig()
        self.client = A2AClient(self.config)
    
    def test_client_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.client.registry_url, "http://localhost:8000")
        self.assertEqual(self.client.timeout, 30)
        self.assertIsNotNone(self.client.session)
    
    @patch('requests.Session.get')
    def test_get_agents_success(self, mock_get):
        """Test successful agent retrieval"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {"name": "TestAgent", "endpoint": "http://localhost:8001"}
        ]
        mock_get.return_value = mock_response
        
        agents = self.client.get_agents()
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0]["name"], "TestAgent")
    
    @patch('requests.Session.get')
    def test_get_agents_failure(self, mock_get):
        """Test agent retrieval failure"""
        # Mock failed response
        mock_get.side_effect = Exception("Connection failed")
        
        with self.assertRaises(click.ClickException):
            self.client.get_agents()

class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    @patch('click.echo')
    def test_print_table_empty(self, mock_echo):
        """Test printing empty table"""
        print_table(["Header1", "Header2"], [])
        mock_echo.assert_called()
    
    @patch('click.echo')
    def test_print_table_with_data(self, mock_echo):
        """Test printing table with data"""
        headers = ["Name", "Status"]
        rows = [["Agent1", "Active"], ["Agent2", "Inactive"]]
        print_table(headers, rows, "Test Table")
        mock_echo.assert_called()

def run_tests():
    """Run all tests and return success status"""
    print("Running A2A CLI Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestA2AConfig))
    suite.addTest(unittest.makeSuite(TestA2AClient))
    suite.addTest(unittest.makeSuite(TestUtilityFunctions))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return True
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} error(s) occurred")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 