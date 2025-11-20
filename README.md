# Advanced Tool Calling with Reasoning Models 

This repository demonstrates advanced function calling techniques with Azure OpenAI, including **parallel tool invocation** and **free-form function calling**. The examples show how to build conversational AI applications that can dynamically call multiple tools/functions, process their outputs, and deliver rich, multi-faceted responses.

---

## Table of Contents

- #overview
- #features
- #file-structure
- #installation
- #usage
- #advantages-of-parallel-and-free-form-tool-calling
- #examples
- #best-practices
- [license
- #contributing
- #contact

---

## Overview

Conversational AI systems often need to interact with external tools or functions to answer complex user queries. This repository provides two Python demos:

- **Single and Parallel Function Calling**: How to invoke a function for each user request, including parallel calls for multiple entities.
- **Free-Form Tool Calling**: How to flexibly parse and handle multiple function calls with varying argument structures, enabling richer and more adaptive conversations.

---

## Features

- **Azure OpenAI Integration**: Easily connect to Azure OpenAI for chat completions and tool calling.
- **Timezone and Weather Utilities**: Example functions for retrieving current time and weather in various cities.
- **Parallel Function Calling**: Efficiently handle multiple requests in a single user query.
- **Free-Form Argument Parsing**: Robustly extract function arguments, even when user input is ambiguous or varied.
- **Extensible Design**: Add new tools/functions with minimal changes.

---

## File Structure

- `function_calling_demo.py`  
  Demonstrates basic and parallel function calling for retrieving the current time in multiple cities.

- `parallel_function_calling_demo.py`  
  Showcases free-form tool calling, handling both weather and time queries in parallel, with flexible argument parsing.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo>
