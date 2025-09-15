from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Train, Section, TrackSegment, TrainType, TrainStatus
from optimization import OptimizationEngine
from .data_service import DataService

def create_app():
    """Create and configure the Flask application"""
    # Set template directory to project root/templates
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'railway-control-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize data service and optimization engine
    data_service = DataService()
    section = data_service.get_sample_section()
    optimization_engine = OptimizationEngine(section)
    
    @app.route('/')
    def dashboard():
        """Main dashboard view"""
        return render_template('dashboard.html')
    
    @app.route('/api/section')
    def get_section_info():
        """Get section information"""
        return jsonify(section.to_dict())
    
    @app.route('/api/trains')
    def get_trains():
        """Get current trains in the section"""
        trains = data_service.get_sample_trains()
        return jsonify([train.to_dict() for train in trains])
    
    @app.route('/api/optimize', methods=['POST'])
    def optimize_schedule():
        """Run optimization and return recommendations"""
        try:
            # Get trains data
            trains = data_service.get_sample_trains()
            
            # Apply any requested modifications (delays, etc.)
            if request.is_json:
                modifications = request.get_json()
                trains = data_service.apply_modifications(trains, modifications)
            
            # Run optimization
            result = optimization_engine.optimize(trains)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error_message': str(e)
            }), 500
    
    @app.route('/api/simulate', methods=['POST'])
    def simulate_scenario():
        """Run what-if scenario simulation"""
        try:
            scenario_data = request.get_json() if request.is_json else {}
            scenario_name = scenario_data.get('scenario_name', 'Custom Scenario')
            
            # Create scenario trains based on parameters
            trains = data_service.create_scenario_trains(scenario_data)
            
            # Run simulation
            result = optimization_engine.simulate_scenario(trains, scenario_name)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error_message': str(e)
            }), 500
    
    @app.route('/api/history')
    def get_optimization_history():
        """Get optimization history"""
        limit = request.args.get('limit', 10, type=int)
        history = optimization_engine.get_optimization_history(limit)
        return jsonify(history)
    
    @app.route('/api/status')
    def get_system_status():
        """Get current system status"""
        status = optimization_engine.get_section_status()
        return jsonify(status)
    
    @app.route('/api/train/<train_id>')
    def get_train_details(train_id):
        """Get detailed information for a specific train"""
        trains = data_service.get_sample_trains()
        train = next((t for t in trains if t.train_id == train_id), None)
        
        if not train:
            return jsonify({'error': 'Train not found'}), 404
            
        return jsonify(train.to_dict())
    
    @app.route('/api/recommendations')
    def get_latest_recommendations():
        """Get latest optimization recommendations"""
        history = optimization_engine.get_optimization_history(1)
        if history:
            return jsonify(history[0].get('recommendations', []))
        else:
            return jsonify([])
    
    @app.route('/api/metrics')
    def get_performance_metrics():
        """Get performance metrics"""
        # Get latest optimization result
        history = optimization_engine.get_optimization_history(1)
        if history:
            metrics = history[0].get('metrics', {})
            # Add current timestamp
            metrics['current_time'] = datetime.now().isoformat()
            return jsonify(metrics)
        else:
            return jsonify({
                'current_time': datetime.now().isoformat(),
                'message': 'No optimization data available'
            })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

def main():
    """Run the Flask application"""
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    
    print(f"\n🚂 Railway Traffic Control System")
    print(f"📍 Running on http://{host}:{port}")
    print(f"📊 Dashboard: http://{host}:{port}/")
    print(f"🔧 API docs available at endpoints starting with /api/")
    print(f"\nPress Ctrl+C to stop the server\n")
    
    app.run(host=host, port=port, debug=app.config['DEBUG'])

if __name__ == '__main__':
    main()
