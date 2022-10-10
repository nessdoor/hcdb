{ lib, python3 }:

python3.pkgs.buildPythonApplication {
  pname = "hcdb";
  version = "0.1";

  src = ./.;

  propagatedBuildInputs = with python3.pkgs; [ pure-cdb ];

  doCheck = false;

  meta = with lib; {
    description = "A usable CLI application to manipulate constant databases";
    license = licenses.gpl3;
  };
}
