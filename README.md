# AutoEC

**AutoEC** is an open-source **automated pumping and switching system** designed to support **batch electrochemical testing of electrolytes through membrane electrode assemblies (MEAs)**.

The system was developed to enable reproducible, programmable control of fluid handling during electrochemical experiments, particularly where repeated electrolyte exchange, flow control, and test cycling are required.

This repository contains control software, test scripts, mechanical design assets, and documentation describing the AutoEC prototype platform.

---

## Project objectives

- Automate fluid handling for electrochemical testing
- Enable programmable control of pumps and switching sequences
- Improve repeatability and throughput in batch MEA experiments
- Provide a flexible platform for rapid experimental iteration

---

## System overview

AutoEC integrates:

### Control software
- **Python-based host control scripts** for pump actuation and experiment sequencing
- Modular test scripts used to validate hardware functionality
- A high-level control interface for coordinating fluid handling steps

### Pump control
- Syringe pumps are controlled using the open-source **`runze-control` Python library**, developed by **Allen Institute / AllenNeuralDynamics**
- This library provides the low-level serial communication and command abstraction for Runze syringe pumps

### Mechanical system
- CAD parts and assemblies (`.ipt`, `.iam`) supporting:
  - Syringe pump frames and holders
  - Structural frames and chamber fixtures
  - Z-axis bars and mounting components

---

## Dependencies

AutoEC relies on the following external libraries:

### Required
- **runze-control**  
  Pump control library for Runze syringe pumps  
  Developed and maintained by **AllenNeuralDynamics**  
  https://github.com/AllenNeuralDynamics/runze-control

- **pyserial**  
  Required for serial communication with pump hardware

Install dependencies using:
```bash
pip install pyserial
pip install git+https://github.com/AllenNeuralDynamics/runze-control.git
