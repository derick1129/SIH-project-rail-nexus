# 🚂 Railway Traffic Control System - MVP

**AI-Powered Precise Train Traffic Control for Indian Railways**

An intelligent decision-support system for railway section controllers to optimize train scheduling and minimize conflicts using priority-based algorithms and real-time optimization.

## 🎯 Project Overview

This MVP demonstrates a simplified but functional railway traffic control system that can:

- **Detect scheduling conflicts** between trains on a linear section
- **Optimize train schedules** using priority-based algorithms
- **Provide real-time recommendations** to section controllers
- **Support what-if scenario analysis** for operational planning
- **Track performance metrics** and system utilization

## 🏗️ Architecture

### Core Components

1. **Data Models** (`src/models/`)
   - Train, Section, Track Segment, and Conflict classes
   - Priority-based train classification (Express > Passenger > Freight)

2. **Optimization Engine** (`src/optimization/`)
   - Conflict detection algorithms
   - Priority-based scheduling with linear programming
   - Real-time recommendation generation

3. **Web Interface** (`src/interface/`)
   - Flask-based dashboard for section controllers
   - Real-time train status and recommendations
   - Interactive scenario simulation

4. **Sample Data** (`data/sample/`)
   - Realistic test scenarios
   - Performance benchmarking tools

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone and setup the project:**
   ```bash
   cd railway_traffic_control
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Or install in development mode
   pip install -e .
   ```

2. **Run the web interface:**
   ```bash
   python -m src.interface.app
   ```

3. **Access the dashboard:**
   Open your browser and navigate to: `http://127.0.0.1:5000`

### Testing Scenarios

Run the sample scenarios to see the system in action:

```bash
python data/sample/sample_scenarios.py
```

This will run three test scenarios:
- **High Congestion Test**: 10 trains with multiple conflicts
- **Platform Bottleneck Test**: Platform capacity optimization  
- **Express Priority Test**: Priority-based conflict resolution

## 🎮 Using the System

### Web Dashboard Features

1. **Current Trains Panel**
   - View all trains in the section
   - See train types, schedules, and current status
   - Monitor delays and priority scores

2. **Section Metrics Panel**
   - Track section utilization and performance
   - Monitor on-time percentages
   - View conflict statistics

3. **Control Recommendations Panel**
   - Get AI-powered scheduling recommendations
   - Run optimization algorithms
   - Simulate different scenarios

### Key Operations

- **🔄 Refresh**: Update train data and metrics
- **⚡ Optimize**: Run conflict detection and resolution
- **🎯 Run Simulation**: Test high-traffic scenarios
- **🗑️ Clear History**: Reset recommendations

## 📊 Sample Scenarios

### Mumbai Central West Section

The MVP simulates a simplified version of a busy Indian railway section with:

- **5 Track Segments**: 3 main tracks + 2 platforms
- **Multiple Train Types**: Express, Passenger, and Freight trains
- **Realistic Scheduling**: Based on Indian Railway operational patterns

### Train Priority System

1. **Express Trains** (Priority: 300)
   - Highest priority for long-distance services
   - Prefer non-platform tracks when available
   - Minimal dwell time

2. **Passenger Trains** (Priority: 200)
   - Medium priority for local services
   - Require platform access
   - Longer dwell times

3. **Freight Trains** (Priority: 100)
   - Lowest priority, can be delayed
   - Use freight sidings when possible
   - Flexible scheduling

## 🔧 API Endpoints

The system provides RESTful APIs for integration:

- `GET /api/trains` - Get current trains
- `GET /api/section` - Get section information  
- `POST /api/optimize` - Run optimization
- `POST /api/simulate` - Run scenario simulation
- `GET /api/metrics` - Get performance metrics
- `GET /api/recommendations` - Get latest recommendations

## 📈 Performance Metrics

The system tracks several key performance indicators:

### Train Metrics
- Total trains in section
- On-time percentage
- Average delay per train type
- Priority score distribution

### Section Metrics
- Track utilization rate
- Available capacity
- Peak usage times
- Conflict frequency

### Optimization Metrics
- Processing time for decisions
- Conflict resolution rate
- Throughput improvement
- Recommendation accuracy

## 🧪 Testing and Validation

### Automated Test Scenarios

1. **High Congestion (10 trains)**
   - Tests system under heavy load
   - Multiple simultaneous conflicts
   - Priority-based resolution

2. **Platform Bottleneck (5 trains)**
   - Platform capacity optimization
   - Queue management algorithms
   - Resource allocation efficiency

3. **Express Priority (6 trains)**
   - Priority enforcement testing
   - Mixed train type handling
   - Dynamic rescheduling

### Success Criteria

- ✅ Conflict detection accuracy > 95%
- ✅ Optimization processing time < 500ms
- ✅ Throughput improvement 10-20%
- ✅ Web interface response time < 2s

## 🚀 Future Enhancements

### Phase 2 Features
- Multiple section coordination
- Real-time data integration
- Advanced ML algorithms
- Mobile interface for field controllers

### Phase 3 Features
- Weather and maintenance integration
- Predictive delay modeling
- Automated decision execution
- Performance analytics dashboard

## 🛠️ Development

### Project Structure
```
railway_traffic_control/
├── src/
│   ├── models/          # Data models and enums
│   ├── optimization/    # Algorithms and engines
│   ├── interface/       # Web app and API
│   └── data/           # Data management
├── data/
│   ├── sample/         # Test scenarios
│   └── schemas/        # Data schemas
├── tests/              # Unit tests
├── docs/               # Documentation
└── config/             # Configuration files
```

### Adding New Features

1. **New Train Types**: Extend `TrainType` enum in `models/enums.py`
2. **Custom Algorithms**: Add to `optimization/` package
3. **API Endpoints**: Extend `interface/app.py`
4. **Test Scenarios**: Add to `data/sample/`

### Configuration

Environment variables in `.env`:
- `FLASK_DEBUG=True` - Enable debug mode
- `PORT=5000` - Web server port
- `DATABASE_URL` - Database connection (future)

## 📝 License

This project is developed for the Ministry of Railways hackathon and demonstrates AI-powered railway traffic optimization concepts.

## 🤝 Contributing

This is an MVP developed for demonstration purposes. For production deployment, additional features like security, scalability, and integration with existing railway systems would be required.

---

**Built with ❤️ for Indian Railways - Making train travel more efficient and punctual**

## 🔗 Quick Links

- 🌐 [Web Dashboard](http://127.0.0.1:5000)
- 📊 [API Documentation](http://127.0.0.1:5000/api/)
- 🧪 [Test Scenarios](./data/sample/sample_scenarios.py)
- 📖 [Architecture Guide](./docs/MVP_ARCHITECTURE.md)
