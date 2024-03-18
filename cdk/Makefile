.PHONY: all

AWS_PROFILE=whillas

deploy:
	cdk deploy --profile $(AWS_PROFILE)

task-update:
	# Force the ECS service to update from new imge
	aws ecs update-service --cluster DjangoCluster --service DjangoFargateService --force-new-deployment --region ap-southeast-2 --profile $(AWS_PROFILE)

redeploy:
	cdk deploy --profile $(AWS_PROFILE)
	deploy