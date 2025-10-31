.PHONY: help clean zip deploy logs

help:
	@echo "Доступные команды:"
	@echo "  make zip     - Создать function.zip для деплоя"
	@echo "  make clean   - Удалить function.zip"
	@echo "  make deploy  - Задеплоить через gcloud CLI"
	@echo "  make logs    - Посмотреть логи функции"

clean:
	@rm -f function.zip
	@echo "✓ function.zip удален"

zip: clean
	@echo "Создание function.zip..."
	@zip -r function.zip . \
		-x "*.git*" ".git/*" \
		-x "*.env*" ".env" \
		-x "*.pyc" "__pycache__/*" \
		-x "*.md" "Makefile" \
		-x ".DS_Store" \
		-x ".idea/*" "*.idea*" \
		-x ".venv/*" "venv/*" \
		-x ".gcloudignore" ".gitignore" ".cloudignore" \
		-x "function.zip"
	@echo "✓ function.zip создан"

deploy:
	@if [ -z "$$FUNCTION_NAME" ]; then \
		echo "Установите переменные окружения:"; \
		echo "  export FUNCTION_NAME=classic-haiku-bot"; \
		echo "  export REGION=us-central1"; \
		exit 1; \
	fi
	gcloud functions deploy $$FUNCTION_NAME \
		--gen2 \
		--runtime=python312 \
		--region=$$REGION \
		--source=. \
		--entry-point=handler \
		--trigger-http \
		--allow-unauthenticated \
		--set-env-vars TOKEN="$$TOKEN",CALENDAR_IMAGE_HOST="$$CALENDAR_IMAGE_HOST"

logs:
	@if [ -z "$$FUNCTION_NAME" ]; then \
		echo "Установите: export FUNCTION_NAME=classic-haiku-bot REGION=us-central1"; \
		exit 1; \
	fi
	gcloud functions logs read $$FUNCTION_NAME --region=$$REGION --gen2 --limit=50
