#!/bin/bash -eux

#echo "Build and publish docker image $IMAGE to $REGISTRY"
#az acr build \
#  --registry $REGISTRY \
#  --image $IMAGE .

#echo "Create container group $CONTAINER_GROUP using YAML file"
#az container create \
#  --resource-group "$RESOURCE_GROUP" \
#  --subscription "$SUBSCRIPTION" \
#  --file "$YAML_CONFIG" \
#  --verbose

#echo "Start container $CONTAINER_GROUP"
#az container start -n "$CONTAINER_GROUP" \
#  --resource-group "$RESOURCE_GROUP" \
#  --subscription "$SUBSCRIPTION" \
#  --verbose --debug

#echo "Follow logs for container $CONTAINER_GROUP"
az container logs \
  --resource-group "$RESOURCE_GROUP" \
  --name "$CONTAINER_GROUP" \
  --subscription "$SUBSCRIPTION" \
  --follow

# Assign security role to a principal.
#az role assignment create \
#  --role Contributor \
#  --assignee $PRINCIPAL \
#  --subscription $SUBSCRIPTION \
#  --scope $APP_SCOPE

# TODO: Clean up resources
#az container delete \
#  --name $CONTAINER_GROUP \
#  --resource-group $RESOURCE_GROUP \
#  --subscription $SUBSCRIPTION