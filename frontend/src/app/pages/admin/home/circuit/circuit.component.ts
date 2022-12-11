import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Circuit } from '@app/models/circuit';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-circuit',
  templateUrl: './circuit.component.html',
  styleUrls: ['./circuit.component.less']
})
export class CircuitComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")?.replace('"', '')
  })

  all_circuit: Circuit[] = []
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
        title: [null, [Validators.required]],
        description: [null, [Validators.required]],
      });  }

  ngOnInit(): void {
    console.log(localStorage.getItem("token"))
    this.http.get<any>(`${BASE_URL}/v1/circuits`, this.options).subscribe(
      data => this.all_circuit = data,
      error => console.error("error as ", error)
    );
  }
  showConfirm(title?: string, uuid?: number): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        console.log(this.options)
        this.http.delete<any>(`${BASE_URL}/v1/circuits?circuit_id=`+uuid, this.options).subscribe(
          data => this.all_circuit = data,
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
      }
      if (this.isEdit){
        const formData = new FormData(); 
        if (this.url !== "assets/images/profil.png"){
          formData.append("uploaded_file", this.uploadedImage)
          this.http.post<any>(`${BASE_URL}/v1/upload/?image_name=`+this.form.value.title,formData, this.options).subscribe(
            data => {
              if(data){
                  const body = {
                    title: this.form.value.title,
                    description: this.form.value.description,
                    url_image: data.filename,
                  }
                  this.http.put<Circuit[]>(`${BASE_URL}/v1/circuits/?circuit_id=`+this.uuid ,body, this.options).subscribe(
                    data => {
                        this.all_circuit = data
                    }, 
                    error => console.error("error as ", error))
              }
            }, 
            error => console.error("error as ", error)
            )
    }
       
      }else{
        if (this.url !== "assets/images/profil.png"){
          const formData = new FormData(); 
          formData.append("uploaded_file", this.uploadedImage)
          this.http.post<any>(`${BASE_URL}/v1/upload/?image_name=`+this.form.value.title,formData, this.options).subscribe(
            data => {
              if(data){
                  const body = {
                    title: this.form.value.title,
                    description: this.form.value.description,
                    url_image: data.filename,
                  }
                  this.http.post<Circuit[]>(`${BASE_URL}/v1/circuits`,body, this.options).subscribe(
                    data => {
                        this.all_circuit = data
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
    this.form.get('title')?.setValue('');
  }

  async showModalEdit(uuid: number){
    this.isEdit = true
    this.uuid = uuid
    this.http.get<Circuit>(`${BASE_URL}/v1/circuits/`+uuid, this.options).subscribe(
      data => {
      this.form.get('title')?.setValue(data.title)
      this.form.get('description')?.setValue(data.description)
      this.url = `${BASE_URL}/v1/image/?image_name=`+data.url_image
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