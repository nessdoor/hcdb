{
  description =
    "Python program to manipulate constant databases, with a humane interface.";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.05";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    
    # This program should be portable enough to be able to run an all main platforms
    flake-utils.lib.eachDefaultSystem (system:
      rec {
        packages.hcdb = nixpkgs.legacyPackages.${system}.callPackage ./package.nix {};
        packages.default = self.packages.${system}.hcdb;
      }
    ) //
    {
      devShells.x86_64-linux.default =
        let pkgs = nixpkgs.legacyPackages."x86_64-linux";
        in
          pkgs.mkShell {
            nativeBuildInputs = with pkgs; [
              (python310.withPackages (pps: with pps; [
                pure-cdb
              ]))

              # Development support
              python310Packages.python-lsp-server
              python310Packages.pyls-isort

              # This is another CDB manipulator, using the original djb interface
              tinycdb
            ];
          };
    };
}
