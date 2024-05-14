{
  description = "gpt-ui";
  inputs = {
    gsay.url = "github:johannesCmayer/gsay"
  };
  outputs = { self, nixpkgs, gsay }: {
    packages.x86_64-linux.default =
      # Notice the reference to nixpkgs here.
      with import nixpkgs { system = "x86_64-linux"; };
  };
}