
export interface User {
  json(): any;
  uuid: string,
  email: string,
  password: string,
  first_name?: string,
  last_name?: string,
  createAt?: string,
  updateAt?: string,
  access_token?: string,
}