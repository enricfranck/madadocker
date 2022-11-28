import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Aventuras } from '@app/models/aventuras';
import { Cars } from '@app/models/car';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from "ng-zorro-antd/modal";

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-cars',
  templateUrl: './cars.component.html',
  styleUrls: ['./cars.component.less']
})
export class CarsComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  all_cars: Cars[] = []
  confirmModal?: NzModalRef 
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  uuid!: number
  url:any ="assets/images/profil.png";
  msg= "";
  options = {
    headers: this.headers
  }

  blob = new Blob(["assets/images/profil.png"])
  uploadedImage: File = new File([this.blob], 'profile.png');
  constructor(private http: HttpClient, private modal: NzModalService, 
    private fb: FormBuilder,)
     {
      this.form = this.fb.group({
        name: [null, [Validators.required]],
      });  }

  ngOnInit(): void {
    
    this.http.get<any>(`${BASE_URL}/v1/cars`, this.options).subscribe(
      data => this.all_cars = data,
      error => console.error("error as ", error)
    );
  }
  showConfirm(name?: string, uuid?: number): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        console.log(this.options)
        this.http.delete<any>(`${BASE_URL}/v1/cars?car_id=`+uuid, this.options).subscribe(
          data => this.all_cars = data,
          error => console.error("error as ", error)
        );
      }
    })
  }

  submitForm(){
    if (this.form.valid) {
      this.isConfirmLoading = true
      const body = {
        name: this.form.value.name,
        description: this.form.value.description,
        direction: this.form.value.direction
      }
      if (this.isEdit){
      }else{
        const formData = new FormData();
        console.log(this.uploadedImage)
          if (this.url !== "assets/images/profil.png"){
            formData.append("uploaded_file", this.uploadedImage)
            this.http.post<any>(`${BASE_URL}/v1/upload/?image_name=`+this.form.value.name,formData, this.options).subscribe(
              data => {
                if(data){
                    const body = {
                      name: this.form.value.name,
                      url_car: data.filename,
                    }
                    this.http.post<Aventuras[]>(`${BASE_URL}/v1/cars`,body, this.options).subscribe(
                      data => {
                          this.all_cars = data
                      }, 
                      error => console.error("error as ", error))
                }
              }, 
              error => console.error("error as ", error)
              )
      }
       
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
    this.form.get('name')?.setValue('');
  }

  async showModalEdit(uuid: number){
    this.isEdit = true
    this.uuid = uuid
    this.http.get<Cars>(`${BASE_URL}/v1/cars/`+uuid, this.options).subscribe(
      data => {
      this.form.get('name')?.setValue(data.name)
      this.url = `${BASE_URL}/cars/image?image_name=`+data.url_car
      },
      error => console.error("error as ", error)
    );
     
    this.isvisible = true
  }


  handleCancel(): void{
    this.isvisible = false
  }

  selectFile(event: any){
    if(!event.target.files[0] || event.target.files[0].length == 0){
      this.msg = "select image"
    }
    var mineType = event.target.files[0].type;
    if(mineType.match(/image\/*/) == null){
      this.msg = "select image"
      this.url ="assets/images/profil.png";
    }
    var reader = new FileReader();
    reader.readAsDataURL(event.target.files[0])

    reader.onload = (_event) =>{
      this.msg = ""
      this.url = reader.result
    } 
    this.uploadedImage = event.target.files[0]
   }

  }
