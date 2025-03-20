{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = with pkgs.python311Packages; [
    jinja2
    fastapi
    uvicorn
    requests_oauthlib
    peewee
    python-multipart
  ] ++ [pkgs.python311];
  idx = {
    extensions = [
      "ms-python.python"
      "ms-python.pylint"
    ];
    workspace = {
      onCreate = {
        install = "";
      };
      onStart = {
        shellCommand = "export PYTHONPATH=$(pwd)/backend";
      };
    };
  };
}