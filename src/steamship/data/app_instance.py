from dataclasses import dataclass

from steamship.base import Client, Request


@dataclass
class CreateAppInstanceRequest(Request):
    id: str = None
    appId: str = None
    appVersionId: str = None
    name: str = None
    handle: str = None
    upsert: bool = None


@dataclass
class DeleteAppInstanceRequest(Request):
    id: str


@dataclass
class AppInstance:
    client: Client = None
    id: str = None
    name: str = None
    handle: str = None
    appId: str = None
    appHandle: str = None
    userHandle: str = None
    appVersionId: str = None
    userId: str = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "AppInstance":
        if 'appInstance' in d:
            d = d['appInstance']

        return AppInstance(
            client=client,
            id=d.get('id', None),
            name=d.get('name', None),
            handle=d.get('handle', None),
            appId=d.get('appId', None),
            appHandle=d.get('appHandle', None),
            userHandle=d.get('userHandle', None),
            appVersionId=d.get('appVersionId', None),
            userId=d.get('userId', None)
        )

    @staticmethod
    def create(
            client: Client,
            appId: str = None,
            appVersionId: str = None,
            name: str = None,
            handle: str = None,
            upsert: bool = None
    ) -> "AppInstance":

        req = CreateAppInstanceRequest(
            name=name,
            handle=handle,
            appId=appId,
            appVersionId=appVersionId,
            upsert=upsert
        )

        return client.post(
            'app/instance/create',
            payload=req,
            expect=AppInstance
        )

    def delete(self) -> "AppInstance":
        req = DeleteAppInstanceRequest(
            id=self.id
        )
        return self.client.post(
            'app/instance/delete',
            payload=req,
            expect=AppInstance
        )

    def get(self, path: str, **kwargs):
        if path[0] == '/':
            path = path[1:]
        return self.client.get(
            '/_/_/{}'.format(path),
            payload=kwargs,
            appCall=True,
            appOwner=self.userHandle,
            appId=self.appId,
            appInstanceId=self.id
        )

    def post(self, path: str, **kwargs):
        if path[0] == '/':
            path = path[1:]
        return self.client.post(
            '/_/_/{}'.format(path),
            payload=kwargs,
            appCall=True,
            appOwner=self.userHandle,
            appId=self.appId,
            appInstanceId=self.id
        )

    def full_url_for(self, path: str, appHandle: str = None, useSubdomain=True):
        if useSubdomain:
            parts = self.client.config.appBase.split("://")
            if parts == 1:
                parts = ["https", parts[0]]
            base = "{}://{}.{}".format(parts[0], self.userHandle, parts[1])
        else:
            base = self.client.config.appBase

        if base[-1] != "/":
            base = "{}/".format(base)

        if useSubdomain is False:
            base = "{}@{}/".format(base, self.userHandle)

        return "{}{}/{}/{}".format(
            base,
            appHandle if appHandle is not None else self.appHandle,
            self.handle,
            path
        )


@dataclass
class ListPrivateAppInstancesRequest(Request):
    pass