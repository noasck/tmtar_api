import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FileResponse, FileService } from '../file.service';

@Component({
  selector: 'app-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.scss'],
})
export class FileComponent implements OnInit {
  errorMessage: string;
  form: FormGroup;
  uploadResponse;
  files: FileResponse[];
  fetchedFile: FormData;

  fileDel: FileResponse;
  indicator: boolean = false;

  url: string = '';

  constructor(
    private fileService: FileService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      avatar: [],
    });

    this.fileService.getFiles().subscribe(
      (res) => {
        this.files = res;
        this.files.map((file) => {
          file.extention = file.filename.substring(
            file.filename.indexOf('.') + 1
          );
        });
      },
      (error) => {
        this.errorMessage = error;
      },
      () => {}
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
      (res) => {
        this.uploadResponse = res;
        res.extention = res.filename.substring(res.filename.indexOf('.') + 1);
        this.files.push(res);
        this.form.get('avatar').setValue([null]);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
  }

  deleteFile(filename) {
    this.fileService.deleteFile(filename).subscribe(
      () => {
        this.files = this.files.filter((file) => file.filename != filename);
      },
      (error) => {
        this.errorMessage = error;
      }
    );
    this.fileDel = null;
  }

  getFileByName(filename) {
    console.log(this.fileService.getFileByName(filename))
    return this.fileService.getFileByName(filename);
  }

  byField(field) {
    if (this.indicator) {
      return (a, b) => (a[field] > b[field] ? -1 : 1);
    } else {
      return (a, b) => (a[field] > b[field] ? 1 : -1);
    }
  }

  sort(field) {
    this.indicator = !this.indicator;
    this.files.sort(this.byField(field));
  }
}
