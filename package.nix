{ lib, python310 }:

python310.pkgs.buildPythonApplication {
  pname = "hcdb";
  version = "0.1";

  src = ./.;

  propagatedBuildInputs = with python310.pkgs; [ pure-cdb ];

  doCheck = false;

  meta = with lib; {
    description = "A usable CLI application to manipulate constant databases";
    license = licenses.gpl3;
  };
}
