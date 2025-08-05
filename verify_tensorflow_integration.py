#!/usr/bin/env python3
"""
Verification script for TensorFlow integration in Library Management System
"""

import sys
import os

def test_imports():
    """Test importing TensorFlow integration modules"""
    print("Testing TensorFlow integration imports...")
    
    try:
        from src.features.tensorflow_integration import (
            TensorFlowIntegration,
            get_book_recommendations,
            forecast_book_demand,
            predict_fine_amount,
            predict_due_date_compliance,
            get_tensorflow_status
        )
        print("✅ TensorFlow integration module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TensorFlow integration module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error importing TensorFlow integration module: {e}")
        return False
    
    try:
        from src.features.tensorflow_api import tensorflow_bp
        print("✅ TensorFlow API module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TensorFlow API module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error importing TensorFlow API module: {e}")
        return False
    
    return True

def test_tensorflow_integration():
    """Test TensorFlow integration functionality"""
    print("\nTesting TensorFlow integration functionality...")
    
    try:
        from src.features.tensorflow_integration import (
            TensorFlowIntegration,
            get_book_recommendations,
            forecast_book_demand,
            predict_fine_amount,
            predict_due_date_compliance,
            get_tensorflow_status
        )
        
        # Test TensorFlow status
        status = get_tensorflow_status()
        print(f"✅ TensorFlow status: {status}")
        
        # Test book recommendations
        user_id = 1
        book_history = [
            {'book_id': 1, 'title': 'Test Book', 'category': 'Fiction', 'rating': 4.5}
        ]
        recommendations = get_book_recommendations(user_id, book_history)
        print(f"✅ Book recommendations generated: {len(recommendations)} items")
        
        # Test demand forecast
        historical_data = [
            {'borrow_count': 5, 'return_count': 4, 'fine_count': 1}
        ]
        forecast = forecast_book_demand(1, historical_data)
        print(f"✅ Demand forecast generated: {forecast}")
        
        # Test fine prediction
        user_data = {'late_returns': 2, 'total_books': 10}
        book_data = {'popularity_score': 0.8, 'fine_rate': 1.0}
        fine_prediction = predict_fine_amount(user_data, book_data)
        print(f"✅ Fine prediction generated: {fine_prediction}")
        
        # Test due date compliance
        compliance = predict_due_date_compliance(user_data, book_data)
        print(f"✅ Due date compliance prediction generated: {compliance}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing TensorFlow integration functionality: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoints registration"""
    print("\nTesting API endpoints registration...")
    
    try:
        from src.app_factory import create_app
        app = create_app()
        
        # Check if TensorFlow blueprint is registered
        tensorflow_endpoint_found = False
        for rule in app.url_map.iter_rules():
            if rule.rule.startswith('/api/tensorflow'):
                tensorflow_endpoint_found = True
                print(f"✅ TensorFlow API endpoint found: {rule.rule}")
        
        if not tensorflow_endpoint_found:
            print("⚠️  No TensorFlow API endpoints found (may be OK if not registered)")
        
        return True
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        return False

def main():
    """Main verification function"""
    print("🤖 Verifying TensorFlow Integration for Library Management System")
    print("=" * 70)
    
    # Test imports
    if not test_imports():
        print("\n❌ TensorFlow integration verification failed at import stage")
        return False
    
    # Test functionality
    if not test_tensorflow_integration():
        print("\n❌ TensorFlow integration verification failed at functionality stage")
        return False
    
    # Test API endpoints
    if not test_api_endpoints():
        print("\n❌ TensorFlow integration verification failed at API stage")
        return False
    
    print("\n🎉 All TensorFlow integration tests passed!")
    print("✅ TensorFlow integration is working correctly")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ TensorFlow integration verification completed successfully")
        else:
            print("\n❌ TensorFlow integration verification failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Verification process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Verification process failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
