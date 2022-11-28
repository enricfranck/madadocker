import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '@environments/environment';
import { User } from '@app/models';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private userSubject: BehaviorSubject<User | null>;
  public user: Observable<User | null >;
  private headersLogin =  new HttpHeaders({
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
  })

  constructor(private router: Router, private http: HttpClient) {
    this.userSubject = new BehaviorSubject<User | null>(
      JSON.parse(localStorage.getItem('user') || 'null')
    );
    this.user = this.userSubject.asObservable();
  }

  public get userValue(): User | null {
    return this.userSubject.value;
  }

  login(email: string, password: string) {
    let body = new URLSearchParams()
    body.set("username", email);
    body.set("password", password);

    let optionsLogin = {
      headers: this.headersLogin
    }

    return this.http.post<User>(`${BASE_URL}/token`, body.toString(), optionsLogin).pipe(
      map((user: any) => {
          console.error(user)
          localStorage.setItem('token', JSON.stringify(user.access_token));
          localStorage.setItem('user', JSON.stringify(user));
          this.userSubject.next(user)
      }))
  }

  logout() {
    // remove user from local storage and set current user to null
    localStorage.removeItem('user');
    this.userSubject.next(null);
    this.router.navigate(['/auth/login']);
  }

  register(user: User) {
    return this.http.post(`${BASE_URL}/users/register`, user);
  }

  getAll() {
    return this.http.get<User[]>(`${BASE_URL}/users/get_all`);
  }

  getById(id: string) {
    return this.http.get<User>(`${BASE_URL}/users/${id}`);
  }

  update(params: any, old_password: string) {
    console.error(params)
    return this.http.put(`${BASE_URL}/users/me?new_password=`+params+'&old_password='+old_password, {}).pipe(
      map((x) => {
        // update stored user if the logged in user updated their own record
        if (x) {
          // update local storage
          const user = { ...this.userValue, ...params };
          localStorage.setItem('user', JSON.stringify(user));

          // publish updated user to subscribers
          this.userSubject.next(user);
        }
        return x;
      })
    );
  }

  delete(id: string) {
    return this.http.delete(`${BASE_URL}/users/${id}`).pipe(
      map((x) => {
        // auto logout if the logged in user deleted their own record
        if (id === this.userValue?.uuid) {
          this.logout();
        }
        return x;
      })
    );
  }
}
