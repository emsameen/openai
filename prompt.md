Define feature scenarios using Cucumber and Gherkin and create C++ tests for each case 
        using the GoogleTest Framework for the following requirements: 
        
.. sys_req:: Brake Light Control Based on Acceleration
   :id: SYSRQ_EXAMPLE_1
   :status: Accepted
   :tags: example, sys_req, valid
   :links: CSTRQ_EXAMPLE_1


   **Purpose:**
   The application will control the brake light based on vehicle deceleration or acceleration, determined using acceleration data collected over a fixed time window.

   **Functional Requirements:**
   The app shall continuously receive real-time acceleration values from a sensor. It shall collect and store a rolling history of acceleration values over a fixed time window of 5 seconds. Using this historical data, the app shall calculate the average or trend of acceleration to determine whether the vehicle is accelerating or decelerating. The app shall turn the brake light ON if the calculated trend or average acceleration value over the 5-second window falls below a specified deceleration threshold. It shall turn the brake light OFF if the trend or average over the same window indicates the vehicle is no longer decelerating.

   **Non-Functional Requirements:**
   The app shall process and update historical data with a latency of no more than 50 milliseconds. It shall run continuously and handle edge cases like sensor disconnection or invalid data inputs.


   **Threshold Values:**
   The deceleration threshold for turning the brake light ON is an average or trend of -2.5 m/s² over the fixed 5-second window. The threshold for turning the brake light OFF is an average or trend above -2.5 m/s².

   **Error Handling:**
   If the sensor data is invalid or unavailable, the app shall maintain the current state of the brake light until valid data is received. If the historical data becomes insufficient due to missing inputs, the app shall default to using the most recent valid acceleration value for decision-making.
for the 
        source code:
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