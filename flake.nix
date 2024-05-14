{
  description = "gpt-ui";
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.11";
    gsay.url = "github:johannesCmayer/gsay";
  };
  outputs = { self, nixpkgs, gsay }: {
    packages.x86_64-linux.default =
      # Notice the reference to nixpkgs here.
      with import nixpkgs { system = "x86_64-linux"; };
      callPackage ./app.nix { inherit gsay; };
  };
}