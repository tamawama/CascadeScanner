{
  description = "A Nix-flake-based Python development environment";
  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          venvDir = ".venv";
          packages = with pkgs; [ python312 xdotool xorg.xprop gtk3 ] ++
            (with pkgs.python312Packages; [
              pip
              venvShellHook
              pygobject3
              pycairo
              requests
              pywlroots
              pywayland
              tkinter
            ]);
        };
      });
    };
}
