import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { User } from '@app/models';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { environment } from '@environments/environment';
import { Aventuras } from '@app/models/aventuras';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-aventure',
  templateUrl: './aventure.component.html',
  styleUrls: ['./aventure.component.less']
})
export class AventureComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")?.replace('"', '')
  })

  all_aventuras: Aventuras[] = []
  confirmModal?: NzModalRef 
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  uuid!: number
  options = {
    headers: this.headers
  }
  constructor(private http: HttpClient, private modal: NzModalService, 
    private fb: FormBuilder,)
     {
      this.form = this.fb.group({
        title: [null, [Validators.required]],
        direction: [null, [Validators.required]],
        description: [null, [Validators.required]],
      });  }

  ngOnInit(): void {
    console.log(localStorage.getItem("token"))
    this.http.get<any>(`${BASE_URL}/v1/aventuras`, this.options).subscribe(
      data => this.all_aventuras = data,
      error => console.error("error as ", error)
    );
  }
  showConfirm(title?: string, uuid?: number): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        console.log(this.options)
        this.http.delete<any>(`${BASE_URL}/v1/aventuras?aventura_id=`+uuid, this.options).subscribe(
          data => this.all_aventuras = data,
          error => console.error("error as ", error)
        );
      }
    })
  }

  submitForm(){
    if (this.form.valid) {
      this.isConfirmLoading = true
      const body = {
        title: this.form.value.title,
        description: this.form.value.description,
        direction: this.form.value.direction
      }
      if (this.isEdit){
        
      }else{
        this.http.post<Aventuras[]>(`${BASE_URL}/v1/aventuras`,body, this.options).subscribe(
          data => {
              this.all_aventuras = data
          }, 
          error => console.error("error as ", error))
      }
      
      this.isvisible = false,
      this.isConfirmLoading = false
    } else {
      Object.values(this.form.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
  }

  showModal(): void{
    this.isEdit = false;
    this.isvisible = true;
    this.form.get('title')?.setValue('');
  }

  async showModalEdit(uuid: number){
    this.isEdit = true
    this.uuid = uuid
    this.http.get<Aventuras>(`${BASE_URL}/v1/aventuras/`+uuid, this.options).subscribe(
      data => {
      this.form.get('title')?.setValue(data.title)
      this.form.get('description')?.setValue(data.description)
      this.form.get('direction')?.setValue(data.direction)
      },
      error => console.error("error as ", error)
    );
     
    this.isvisible = true
  }


  handleCancel(): void{
    this.isvisible = false
  }

  }