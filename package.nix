{ lib, buildPythonApplication, pure-cdb }:

buildPythonApplication {
  pname = "hcdb";
  version = "0.1";

  src = ./.;

  propagatedBuildInputs = [ pure-cdb ];

  doCheck = false;

  meta = with lib; {
    description = "A usable CLI application to manipulate constant databases";
    license = licenses.gpl3;
  };
}
