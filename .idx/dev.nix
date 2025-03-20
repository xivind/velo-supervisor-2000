{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = with pkgs.python311Packages; [
    python311
    jinja2
    fastapi
    uvicorn
    requests_oauthlib
    peewee
    python-multipart
  ];
  idx = {
    extensions = [ "ms-python.python" ];
    workspace = {
      onCreate = {
        install = "";
      };
    };
  };
}