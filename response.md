Certainly, Developer! Below, I'll define feature scenarios using Cucumber and Gherkin syntax based on the given brake light control requirements. Following that, I'll create corresponding C++ tests using the GoogleTest framework.

### Feature Scenarios in Gherkin

```gherkin
Feature: Brake Light Control Based on Acceleration
  As a vehicle control system
  I want to control the brake light based on acceleration data
  So that the brake light informs other drivers when the vehicle is decelerating

  Background:
    Given a brake light controller is initialized

  Scenario: Brake light should turn ON when deceleration is below threshold
    When I add acceleration value -3.0
    Then the brake light should be ON

  Scenario: Brake light should turn OFF when deceleration is above threshold
    Given the brake light is ON
    When I add acceleration value -1.0
    Then the brake light should be OFF

  Scenario: Maintain brake light state when sensor is disconnected
    Given I add acceleration value -3.0
    And the sensor is disconnected
    When I add acceleration value -1.0
    Then the brake light should be ON

  Scenario: Use last valid acceleration if history is insufficient
    Given I have added 3 acceleration values: -3.0, -2.0, 0.0
    When I add acceleration value -1.0
    Then the brake light should remain ON

  Scenario: Ignore invalid acceleration values
    Given I add acceleration value -3.0
    When I add acceleration value NaN
    Then the brake light should remain ON
```

### C++ Tests using GoogleTest Framework

Here’s how you can implement these scenarios in C++ with GoogleTest:

```cpp
#include <gtest/gtest.h>
#include <cmath> // For std::isnan

class BrakeLightControllerTest : public ::testing::Test {
protected:
    BrakeLightController controller;

    void SetUp() override {
        // Initial state is off
        controller = BrakeLightController();
    }
};

TEST_F(BrakeLightControllerTest, BrakeLightTurnsOn) {
    controller.addAcceleration(-3.0);
    EXPECT_TRUE(controller.isBrakeLightOn());
}

TEST_F(BrakeLightControllerTest, BrakeLightTurnsOff) {
    controller.addAcceleration(-3.0);
    EXPECT_TRUE(controller.isBrakeLightOn()); // Should be ON
    controller.addAcceleration(-1.0);
    EXPECT_FALSE(controller.isBrakeLightOn()); // Should be OFF
}

TEST_F(BrakeLightControllerTest, MaintainStateWhenSensorDisconnected) {
    controller.addAcceleration(-3.0);
    EXPECT_TRUE(controller.isBrakeLightOn()); // Should be ON
    controller.setSensorState(false);
    controller.addAcceleration(-1.0);
    EXPECT_TRUE(controller.isBrakeLightOn()); // Should remain ON due to disconnection
}

TEST_F(BrakeLightControllerTest, UseLastValidAccelerationIfHistoryIsInsufficient) {
    controller.addAcceleration(-3.0);
    controller.addAcceleration(-2.0);
    controller.addAcceleration(0.0);
    // Only 3 values added, not enough for a 5s window
    controller.addAcceleration(-1.0);
    EXPECT_TRUE(controller.isBrakeLightOn()); // Should be ON, as it's using last valid
}

TEST_F(BrakeLightControllerTest, IgnoreInvalidAccelerationValues) {
    controller.addAcceleration(-3.0);
    EXPECT_TRUE(controller.isBrakeLightOn()); // Should be ON
    controller.addAcceleration(NAN); // Invalid input
    EXPECT_TRUE(controller.isBrakeLightOn()); // Should remain ON
}
```

### Explanation

1. **Feature Scenarios**: These Gherkin scenarios outline different behaviors of the `BrakeLightController` based on the input acceleration values. 

2. **C++ Tests**: Each test corresponds to a specific scenario, invoking methods on the `BrakeLightController` and verifying the expected states of the brake light.

3. **Setup and Assertions**: The `SetUp` function initializes the `BrakeLightController`, and assertions are used to validate the expected states.

Feel free to expand or modify these scenarios and tests based on additional requirements or specific edge cases you may encounter in your system!