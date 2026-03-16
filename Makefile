## 基本操作
init:
	@echo "$(BLUE)🔨 初始化資料庫...$(RESET)"
	docker-compose up airflow-init
	@echo "$(GREEN)✅ 初始化完成！$(RESET)"

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

clean:
	docker-compose down --volumes --rmi all