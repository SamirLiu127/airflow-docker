# Data Mining Airflow 專案 Makefile

.PHONY: help up down restart clean logs shell test build
.DEFAULT_GOAL := help

# 顏色設定
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# 專案設定
AIRFLOW_UID := $(shell id -u)

## 顯示說明
help:
	@echo "$(BLUE)🚁 Airflow 開發工具$(RESET)"
	@echo ""
	@echo "$(GREEN)🚀 快速開始:$(RESET)"
	@echo "  $(YELLOW)make quickstart$(RESET)              - 一鍵建立並啟動所有服務"
	@echo "  $(YELLOW)make up$(RESET)                     - 啟動已建立的服務"
	@echo "  $(YELLOW)make down$(RESET)                   - 停止所有服務"
	@echo ""
	@echo "$(GREEN)⚡ 日常開發:$(RESET)"
	@echo "  $(YELLOW)make dag-list$(RESET)               - 查看所有 DAG"
	@echo "  $(YELLOW)make dag-trigger DAG_ID=simple_dag$(RESET) - 手動觸發 DAG"
	@echo "  $(YELLOW)make logs$(RESET)                   - 查看即時日誌"
	@echo "  $(YELLOW)make shell$(RESET)                  - 進入 Airflow 容器"
	@echo ""
	@echo "$(GREEN)🔧 維護除錯:$(RESET)"
	@echo "  $(YELLOW)make status$(RESET)                 - 檢查服務狀態"
	@echo "  $(YELLOW)make restart$(RESET)                - 重啟服務"
	@echo "  $(YELLOW)make clean$(RESET)                  - 完全清理重置"
	@echo "  $(YELLOW)make rebuild$(RESET)                - 重建映像檔並重啟"
	@echo ""
	@echo "📱 $(BLUE)Web UI: http://localhost:8080$(RESET) (airflow/airflow)"

## 基本操作
up:
	@echo "$(BLUE)🚀 啟動 Airflow...$(RESET)"
	AIRFLOW_UID=$(AIRFLOW_UID) docker-compose up -d
	@echo "$(GREEN)✅ 啟動完成！$(RESET)"
	@echo "📱 Web UI: http://localhost:8080"

down:
	@echo "$(BLUE)⏹️  停止服務...$(RESET)"
	docker-compose down
	@echo "$(GREEN)✅ 已停止$(RESET)"

restart: down up

logs:
	@echo "$(BLUE)📋 查看日誌...$(RESET)"
	docker-compose logs -f

logs-scheduler:
	@echo "$(BLUE)📋 查看 Scheduler 日誌...$(RESET)"
	docker-compose logs -f airflow-scheduler

shell:
	@echo "$(BLUE)🐚 進入容器...$(RESET)"
	docker-compose exec airflow-apiserver bash

## DAG 管理
dag-list:
	@echo "$(BLUE)📋 DAG 列表:$(RESET)"
	docker-compose exec airflow-apiserver airflow dags list

dag-trigger:
	@if [ -z "$(DAG_ID)" ]; then \
		echo "$(RED)❌ 使用方法: make dag-trigger DAG_ID=simple_dag$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)🚀 觸發 DAG: $(DAG_ID)$(RESET)"
	docker-compose exec airflow-apiserver airflow dags trigger $(DAG_ID)

dag-test:
	@if [ -z "$(DAG_ID)" ]; then \
		echo "$(RED)❌ 使用方法: make dag-test DAG_ID=simple_dag$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)🧪 測試 DAG: $(DAG_ID)$(RESET)"
	docker-compose exec airflow-apiserver airflow dags test $(DAG_ID) 2025-01-01

## 建立和維護
build:
	@echo "$(BLUE)🔨 建立映像檔...$(RESET)"
	AIRFLOW_UID=$(AIRFLOW_UID) docker-compose build

rebuild: clean build up

clean:
	@echo "$(BLUE)🧹 清理資源...$(RESET)"
	docker-compose down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)✅ 清理完成$(RESET)"

## 快速啟動
quickstart: build up
	@echo "$(GREEN)🎉 快速啟動完成！$(RESET)"
	@echo "等待服務啟動..."
	@sleep 30
	@echo "📱 請打開: http://localhost:8080"