export type TokenData = {
  accessToken: string
  idToken: string
}

export type Upload = {
  uploadURI: string
}

export type CreateImage = Upload & { image: Image }

export type CreatePackage = Upload & { package: Package }

export type Image = {
  id: string
  // other properties exist but do not matter here
}

export type Package = {
  id: string
  // other properties exist but do not matter here
}
