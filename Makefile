.PHONY: deploy

deploy: 
	gcloud functions deploy classic-haiku-bot \
  		--source .
  		--entry-point handler \
  		--runtime python37 \
		--memory=128Mb \
  		--trigger-http \
  		--allow-unauthenticated
