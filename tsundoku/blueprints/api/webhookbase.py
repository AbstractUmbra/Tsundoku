import json
from typing import List, Optional

from quart import abort, Response, request, views
from quart import current_app as app
from quart_auth import current_user

from tsundoku.webhooks import WebhookBase


class WebhookBaseAPI(views.MethodView):
    async def get(self, base_id: Optional[int]=None) -> List[dict]:
        """
        Retrieve all WebhookBases.

        Parameters
        ----------
        base_id: Optional[int]
            The specific WebhookBase to retrieve.

        Returns
        -------
        List[dict]
            A list of results.
        """
        if not await current_user.is_authenticated:
            return abort(401, "You are not authorized to access this resource.")

        if not base_id:
            return json.dumps([base.to_dict() for base in await WebhookBase.all()])
        else:
            base = await WebhookBase.from_id(base_id)
            if not base:
                return "[]"
            return json.dumps([base.to_dict()])


    async def post(self) -> dict:
        """
        Adds a new webhook base.

        Valid WebhookBase Services:
        dicord, slack, custom

        Returns
        -------
        dict
            The new webhook.
        """
        if not await current_user.is_authenticated:
            return abort(401, "You are not authorized to access this resource.")

        wh_services = ("discord", "slack", "custom")
        await request.get_data()
        arguments = await request.form

        service = arguments.get("service")
        url = arguments.get("url")

        if service not in wh_services:
            response = {"error": "invalid webhook service"}
            return Response(json.dumps(response), status=400)
        elif not url:
            response = {"error": "invalid webhook url"}
            return Response(json.dumps(response), status=400)

        base = await WebhookBase.new(
            service,
            url
        )

        if base:
            return json.dumps(base.to_dict())
        else:
            return "{}"


    async def put(self, base_id: int) -> dict:
        """
        Updates a specific webhook base.

        Parameters
        ----------
        base_id:
            The ID of the webhook base.

        Returns
        -------
        The updated webhook base.
        """
        if not await current_user.is_authenticated:
            return abort(401, "You are not authorized to access this resource.")

        wh_services = ("discord", "slack", "custom")
        await request.get_data()
        arguments = await request.form

        service = arguments.get("service")
        url = arguments.get("url")
        content_fmt = arguments.get("content_fmt")\

        base = await WebhookBase.from_id(base_id)

        if not base:
            response = {"error": "invalid webhook base"}
            return Response(json.dumps(response), status=400)
        elif service not in wh_services:
            response = {"error": "invalid webhook service"}
            return Response(json.dumps(response), status=400)
        elif not url:
            response = {"error": "invalid webhook url"}
            return Response(json.dumps(response), status=400)
        elif not content_fmt:
            response = {"error": "invalid content format"}
            return Response(json.dumps(response), status=400)

        base.service = service
        base.url = url
        base.content_fmt = content_fmt

        await base.save()

        return json.dumps(base.to_dict())


    async def delete(self, base_id: int) -> Optional[dict]:
        """
        Deletes a single webhook base.

        Parameters
        ----------
        base_id: int
            The ID of the webhook base.

        Returns
        -------
        Optional[dict]
            If the item was deleted, returns
            the item.
        """
        if not await current_user.is_authenticated:
            return abort(401, "You are not authorized to access this resource.")

        base = await WebhookBase.from_id(base_id)
        deleted = await base.delete()

        if deleted:
            return json.dumps(base.to_dict())
        else:
            return "{}"