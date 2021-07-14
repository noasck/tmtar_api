import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-delete-user',
  templateUrl: './delete-user.component.html',
  styleUrls: ['./delete-user.component.scss']
})
export class DeleteUserComponent implements OnInit {
  @Output() deleteOption: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Input() user: number | string;
  validation: string;

  confirmText = new FormControl('', [
    Validators.required
  ])

  constructor() { }

  ngOnInit(): void {
    if(typeof this.user === 'number'){
      this.validation = `delete user ${this.user}`
    }
    else{
      this.validation = `delete users`
    }
    
  }
  pickOption(option: boolean): void {
    if (option === true && this.confirmText.value === this.validation) {
      this.deleteOption.emit(true);
    }
    else {
      this.deleteOption.emit(false);
    }
  }

}
