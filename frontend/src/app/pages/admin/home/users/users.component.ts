import { Component, OnInit } from '@angular/core';
import { User } from '@app/models';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from "ng-zorro-antd/modal";

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.less']
})

export class UsersComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  all_users: User[] = []
  confirmModal?: NzModalRef

  options = {
    headers: this.headers
  }
  constructor(private http: HttpClient, private modal: NzModalService) { }

  ngOnInit(): void {
    
    this.http.get<any>(`${BASE_URL}/aventuras/all`, this.options).subscribe(
      data => this.all_users = data,
      error => console.error("error as ", error)
    );
  }
  showConfirm(name: string, uuid: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/users/?uuid=`+uuid, this.options).subscribe(
          data => this.all_users = data,
          error => console.error("error as ", error)
        );
      }
    })
  }

  }