#include <deque>        // For std::deque
#include <numeric>      // For std::accumulate
#include <cmath>        // For std::isnan

class BrakeLightController {
public:
    void addAcceleration(double acceleration) {
        if (validAcceleration(acceleration)) {
            accelerationHistory.push_back(acceleration);
            if (accelerationHistory.size() > windowSize) {
                accelerationHistory.pop_front();
            }
        } 
        calculateState();
    }

    bool isBrakeLightOn() const {
        return brakeLightOn;
    }

    void setSensorState(bool available) {
        sensorAvailable = available;
        if (!sensorAvailable) {
            // If sensor is disconnected, maintain the current state
            return;
        }
    }

private:
    static constexpr int windowSize = 5; // in seconds
    std::deque<double> accelerationHistory;
    bool brakeLightOn = false;
    bool sensorAvailable = true;
    
    void calculateState() {
        if (!sensorAvailable) return;

        if (accelerationHistory.size() < windowSize) {
            // Use last valid acceleration as default if history is insufficient
            brakeLightOn = (accelerationHistory.back() < -2.5);
        } else {
            double avgAcceleration = std::accumulate(accelerationHistory.begin(), accelerationHistory.end(), 0.0) / accelerationHistory.size();
            brakeLightOn = (avgAcceleration < -2.5);
        }
    }

    bool validAcceleration(double acceleration) {
        // Assume any value other than NaN or absurd values is valid for this example
        return !std::isnan(acceleration);
    }
};