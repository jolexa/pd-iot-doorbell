STACKNAME_BASE="pd-iot-doorbell"
# This is the name of the thing you configured in the AWS Console
THING_NAME="pd-iot-doorbell"
# This is a region that supports AWS IoT
REGION="us-east-2"
# Bucket in REGION that is used for deployment
BUCKET=$(STACKNAME_BASE)
MD5=$(shell md5sum lambda/*.py | md5sum | cut -d ' ' -f 1)
SERIAL=$(shell aws iot describe-thing --region $(REGION) --thing-name $(THING_NAME) --query attributes.serial)

deploy:
	cd lambda && \
		zip -r9 /tmp/deployment.zip *.py && \
		aws s3 cp --region $(REGION) /tmp/deployment.zip \
			s3://$(BUCKET)/$(MD5) && \
		rm -rf /tmp/deployment.zip
	aws cloudformation deploy \
		--template-file deployment.yml \
		--stack-name $(STACKNAME_BASE) \
		--region $(REGION) \
		--parameter-overrides \
		"Bucket=$(BUCKET)" \
		"md5=$(MD5)" \
		"SerialNumber=$(SERIAL)" \
		--capabilities CAPABILITY_IAM || exit 0
