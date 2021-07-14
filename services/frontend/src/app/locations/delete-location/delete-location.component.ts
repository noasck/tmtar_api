import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-delete-location',
  templateUrl: './delete-location.component.html',
  styleUrls: ['./delete-location.component.scss'],
})
export class DeleteLocationComponent implements OnInit {
  @Output() deleteOption: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Input() location: string;
  validation: string;

  confirmText = new FormControl('', [
    Validators.required
  ])

  constructor() { }

  ngOnInit(): void {
    this.validation = `delete location ${this.location}`
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
