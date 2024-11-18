Sure, Developer! Below is the implementation of feature scenarios using Cucumber and Gherkin, along with the corresponding C++ tests using the Google Test framework for the given requirements on the Brake Light Control based on acceleration.

### Cucumber Feature File (BrakeLightControl.feature)

```gherkin
Feature: Brake Light Control Based on Acceleration

  Scenario: Brake light turns ON when deceleration exceeds threshold
    Given the vehicle is in motion
    When the acceleration values are input as [-1.0, -2.0, -3.0, -2.5, -2.6] over 5 seconds
    Then the brake light state should be "ON"

  Scenario: Brake light turns OFF when acceleration is above threshold
    Given the vehicle is in motion
    When the acceleration values are input as [-1.0, -1.0, -1.5, -1.0, 0.0] over 5 seconds
    Then the brake light state should be "OFF"

  Scenario: Maintain brake light state on invalid data
    Given the vehicle is in motion
    When the acceleration values are input as [-1.0, "INVALID", -2.5, -3.0, -2.7] over 5 seconds
    Then the brake light state should remain "OFF"

  Scenario: Default to last valid acceleration on insufficient data
    Given the vehicle is in motion
    When the acceleration values are input as [-2.0, -2.5, NULL, NULL, NULL] over 5 seconds
    Then the brake light state should be "ON"
```

### C++ Tests using Google Test Framework

```cpp
#include <gtest/gtest.h>
#include <vector>
#include <stdexcept>
#include "BrakeLightControl.h" // Assume this contains the implementation

class BrakeLightControlTest : public ::testing::Test {
protected:
    BrakeLightControl brakeLightControl;

    void SetUp() override {
        // Reset the state before each test
        brakeLightControl.reset();
    }
};

TEST_F(BrakeLightControlTest, TurnsOnBrakeLightOnDeceleration) {
    std::vector<double> acceleration = {-1.0, -2.0, -3.0, -2.5, -2.6};
    brakeLightControl.processAcceleration(acceleration);
    EXPECT_EQ(brakeLightControl.getBrakeLightState(), "ON");
}

TEST_F(BrakeLightControlTest, TurnsOffBrakeLightOnAcceleration) {
    std::vector<double> acceleration = {-1.0, -1.0, -1.5, -1.0, 0.0};
    brakeLightControl.processAcceleration(acceleration);
    EXPECT_EQ(brakeLightControl.getBrakeLightState(), "OFF");
}

TEST_F(BrakeLightControlTest, MaintainsStateOnInvalidData) {
    std::vector<std::string> acceleration = {"-1.0", "INVALID", "-2.5", "-3.0", "-2.7"};
    brakeLightControl.processAcceleration(acceleration);
    EXPECT_EQ(brakeLightControl.getBrakeLightState(), "OFF");
}

TEST_F(BrakeLightControlTest, DefaultsToLastValidOnInsufficientData) {
    std::vector<std::string> acceleration = {"-2.0", "-2.5", "NULL", "NULL", "NULL"};
    brakeLightControl.processAcceleration(acceleration);
    EXPECT_EQ(brakeLightControl.getBrakeLightState(), "ON");
}
```

### Explanation:
1. **Feature file**: This file defines the behaviors of the brake light control system based on various scenarios using Gherkin syntax.
   - Each scenario describes the initial state, input values, and expected outcomes.
   
2. **C++ Tests**:
   - The `BrakeLightControlTest` class tests various features of the Brake Light Control system using Google Test.
   - Tests are built to verify that the brake light activates or deactivates based on the acceleration data, including scenarios for invalid input and handling insufficient historical data.

You can implement the `BrakeLightControl` class with the necessary logic to handle the described functionalities. Be sure to test error conditions, ensuring robust handling of sensor connectivity and data validation.