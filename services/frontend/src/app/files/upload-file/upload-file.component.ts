import { Component, OnInit } from '@angular/core';
import { FileService } from '../file.service';
import { FormGroup, FormBuilder } from '@angular/forms';
import { FileResponse } from '../file.service'
@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.scss']
})
export class UploadFileComponent implements OnInit {
  errorMessage: string;
  form: FormGroup;
  uploadResponse;
  files: FileResponse[]

  constructor(private fileService: FileService, private formBuilder: FormBuilder) {
  }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      avatar: []
    });

    this.fileService.getFiles().subscribe(
      (res) => {
        this.files = res;
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {
      }
    );

  }


  onFileChange(event): void {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.form.get('avatar').setValue(file);
    }
  }

  onSubmit(): void {
    let formData = new FormData();
    formData.append('file', this.form.get('avatar').value);
    this.fileService.postFile(formData).subscribe(
      (res) => this.uploadResponse = res,
    );
  }
}
