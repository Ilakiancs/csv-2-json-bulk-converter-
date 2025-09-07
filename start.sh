#!/bin/bash

# CSV to JSON Converter Startup Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}CSV to JSON Converter${NC}"
echo "========================"
echo ""
echo "Choose an option:"
echo -e "${GREEN}1)${NC} Command Line Converter (batch process folders)"
echo -e "${GREEN}2)${NC} Web UI Converter (drag & drop interface)"
echo -e "${GREEN}3)${NC} Install Dependencies"
echo -e "${GREEN}4)${NC} Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo -e "${YELLOW}Starting Command Line Converter...${NC}"
        echo ""
        python3 csv_to_json_converter.py
        ;;
    2)
        echo -e "${YELLOW}Starting Web UI Converter...${NC}"
        echo -e "${BLUE}Open your browser to: http://localhost:8080${NC}"
        echo ""
        python3 ui_converter.py
        ;;
    3)
        echo -e "${YELLOW}Installing dependencies...${NC}"
        pip3 install -r requirements.txt
        echo -e "${GREEN}Dependencies installed successfully!${NC}"
        ;;
    4)
        echo -e "${GREEN}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac
